import os
from azure.keyvault import KeyVaultClient, KeyVaultAuthentication
from azure.common.credentials import ServicePrincipalCredentials

# pip installations apart from azure keyvault and credentials packages
# this is required for SSL certificate when running from local boxes
# pip install  python-certifi-win3


def main():

    def auth_callback(server, resource, scope):
        credentials = ServicePrincipalCredentials(
            client_id=<client-id>,
            secret=<client-secret>,
            tenant=<tenant-id>,
            resource="https://vault.azure.net",
        )
        token = credentials.token

        return token['token_type'], token['access_token']

    client = KeyVaultClient(KeyVaultAuthentication(auth_callback))
    key_vault_dict = {}
    secret_name_list = "my-api-client-secret"

    for i in secret_name_list.split(","):
        secret_t = client.get_secret("https://<domain>.vault.azure.net/", i, "")
        key_vault_dict[i] = secret_t.value

    print(key_vault_dict)


if __name__ == '__main__':
    main()
