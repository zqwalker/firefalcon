import json

import falcon
from firebase_admin.exceptions import AlreadyExistsError, FirebaseError, NotFoundError
from pydantic import ValidationError

from ._schemas import BaseQuerySchema, BaseSchema
from ._utils import create_collection_query
from .authorize import Authorize


class FirstoreBaseResource:
    base_schema = BaseSchema
    base_query_schema = BaseQuerySchema
    authorize = Authorize
    valid_error = ValidationError

    def __init__(
        self,
        db,
        db_path_prefix="",
        db_path=None,
        schema_post=None,
        schema_get=None,
        schema_put=None,
        schema_patch=None,
        schema_q=None,
        allowed=None,
    ):
        self.db = db
        self._db_path = db_path
        self._schema_post = schema_post
        self._schema_get = schema_get
        self._schema_put = schema_put
        self._schema_patch = schema_patch
        self._schema_q = schema_q
        self.allowed = None

    def get_db_path(self, path):
        if self._db_path is None:
            return path[1:]
        else:
            return f"{self.db_path_prefix}{self._db_path}"

    def _validate(self, schema, data):
        try:
            if schema is None:
                return self.base_schema.parse_obj(data)
            return schema.parse_obj(data)

        except self.valid_error as e:
            title = "ValidationError"
            description = str(e)
            raise falcon.HTTPBadRequest(title=title, description=description)

    def _validate_post(self, data):
        return self._validate(self._schema_post, data)

    def _validate_get(self, data):
        return self._validate(self._schema_get, data)

    def _validate_put(self, data):
        return self._validate(self._schema_put, data)

    def _validate_patch(self, data):
        return self._validate(self._schema_patch, data)

    def _validate_q(self, data):
        if self._schema_q is None:
            return self._validate(self.base_query_schema, data)
        return self._validate(self._schema_q, data)

    @falcon.before(authorize("on_get"))
    def on_get(self, req, resp, **kwargs):
        try:
            db_path = self.get_db_path(req.path)
            col_ref = self.db.collection(db_path)

            params = self._validate_q(req.params)
            query_ref = create_collection_query(col_ref, req.params)

            docs = query_ref.stream()
            validated = [self._validate_get(doc.to_dict()).dict() for doc in docs]

            resp.status = falcon.HTTP_200
            resp.media = validated

        except FirebaseError as e:
            raise falcon.HTTPBadRequest(code=e.code, description=e.message)

    @falcon.before(authorize("on_get_doc"))
    def on_get_doc(self, req, resp, **kwargs):
        try:
            db_path = self.get_db_path(req.path)
            doc_ref = self.db.document(db_path)

            doc = doc_ref.get()
            validated = self._validate_get(doc.to_dict())

            resp.status = falcon.HTTP_200
            resp.body = validated.json()

        except FirebaseError as e:
            raise falcon.HTTPBadRequest(code=e.code, description=e.message)

    @falcon.before(authorize("on_post"))
    def on_post(self, req, resp, **kwargs):
        try:
            validated = self._validate_post(req.media)

            db_path = self.get_db_path(req.path)
            col_ref = self.db.collection(db_path)

            if hasattr(validated, "id"):
                doc_ref = col_ref.document(validated.id)
                doc_ref.create(validated.dict())

            else:
                doc_ref = col_ref.document()
                doc_ref.create({"id": doc_ref.id, **validated.dict()})

            resp.status = falcon.HTTP_201
            resp.media = {"id": doc_ref.id}

        except AlreadyExistsError as e:
            raise falcon.HTTPConflict(code=e.code, description=e.message)

        except FirebaseError as e:
            raise falcon.HTTPBadRequest(code=e.code, description=e.message)

    @falcon.before(authorize("on_put_doc"))
    def on_put_doc(self, req, resp, **kwargs):
        try:
            validated = self._validate_put(req.media)

            db_path = self.get_db_path(req.path)
            doc_ref = self.db.document(db_path)

            doc_ref.set(validated.dict())

            resp.status = falcon.HTTP_200
            resp.media = {"id": doc_ref.id}

        except FirebaseError as e:
            raise falcon.HTTPBadRequest(code=e.code, description=e.message)

    @falcon.before(authorize("on_put_doc"))
    def on_patch_doc(self, req, resp, **kwargs):
        try:
            validated = self._validate_patch(req.media)

            db_path = self.get_db_path(req.path)
            doc_ref = self.db.document(db_path)

            doc_ref.update(validated.dict())

            resp.status = falcon.HTTP_200
            resp.media = {"id": doc_ref.id}

        except NotFoundError as e:
            raise falcon.HTTPNotFound(code=e.code, description=e.message)

        except FirebaseError as e:
            raise falcon.HTTPBadRequest(code=e.code, description=e.message)

    @falcon.before(authorize("on_delete_doc"))
    def on_delete_doc(self, req, resp, **kwargs):
        try:
            db_path = self.get_db_path(req.path)
            doc_ref = self.db.document(db_path)

            doc_ref.delete()

        except NotFoundError as e:
            raise falcon.HTTPNotFound(code=e.code, description=e.message)

        except FirebaseError as e:
            raise falcon.HTTPBadRequest(code=e.code, description=e.message)
