server {
	listen 80;
	server_name superlists-staging.nigelharsch.com;

	location /static {
                alias /home/nharsch/sites/superlists-staging.nigelharsch.com/static; 
        }	

	location / {
		proxy_set_header Host $host;
		proxy_pass http://unix:/tmp/superlists-staging.nigelharsch.com.socket;
	}
}
