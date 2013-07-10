# Enter your DataSift username and API key
username    = "user"
api_key     = "api-key"

# Historics paramters
stream_hash                     = "hash"
name                            = "name"

output_params = {}
output_params['file_prefix']    = "prefix"
output_params['directory']      = "/path/to/directory"

# Date format in YYYY-MM-DD HH:MM:SS (UTC)
start_date  = "2013-07-01 00:00:00"         
end_date    = "2013-07-02 00:00:00"

### Do not need to change (often)
sample      = "100" # Sample rate; change to 10 if smaller is needed
sources     = "twitter" # Comma-separated list of sources

output_type = "ftp"

output_params['host']               = "host"
output_params['port']               = 21
output_params['auth.username']      = "username"
output_params['auth.password']      = "password"
output_params['delivery_frequency'] = 0
output_params['max_size']           = 10485760
output_params['format']             = "json_new_line"