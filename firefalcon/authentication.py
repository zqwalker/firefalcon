import falcon

class Authentication:
    def __init__(self, auth):
        self.auth = auth
        
    def process_request(self, req, resp):
        bearer_auth = req.auth

        challenges = ['Token type="Bearer"']

        if bearer_auth is None:
            description = "Please provide an auth token as part of the request."

            raise falcon.HTTPUnauthorized(
                "Auth token required", description, challenges
            )

        try:
            id_token = bearer_auth.split()[1]
            check_token = auth.verify_id_token(id_token, check_revoked=True)

        except:
            description = (
                "The provided auth token has been revoked. "
                "Please request a new token and try again."
            )

            raise falcon.HTTPUnauthorized(
                "Authentication required", description, challenges
            )

        try:
            decoded_token = auth.verify_id_token(id_token)
            req.context.token = decoded_token
            return

        except:
            description = (
                "The provided auth token is not valid. "
                "Please request a new token and try again."
            )

            raise falcon.HTTPUnauthorized(
                "Authentication required", description, challenges
            )