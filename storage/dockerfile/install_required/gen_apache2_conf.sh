if [ $# -ne 2 ]
then
 echo "sh $0 <log_dir> <api_dir>"
 exit
fi
log_dir=$1  # /home/site/html-test/dist
api_dir=$2  # /home/site/api-test/storage/logs/apache2


echo "
<VirtualHost *:9003>
    Alias /static/admin/ /usr/local/lib/python3.6/dist-packages/django/contrib/admin/static/admin/
    Alias /static/rest_framework/ /usr/local/lib/python3.6/dist-packages/rest_framework/static/rest_framework/
    Alias /static/debug_toolbar/ /usr/local/lib/python3.6/dist-packages/debug_toolbar/static/debug_toolbar/
    Alias /static/ /home/site/api/storage/collect_static/

    ServerName crisperdx
    ErrorLog $log_dir/api.crisperdx-error_log
    CustomLog $log_dir/api.crisperdx-access_log common

    WSGIDaemonProcess crisperdx python-path=$api_dir
    WSGIProcessGroup crisperdx
    WSGIScriptAlias / $api_dir/config/wsgi.py process-group=crisperdx
    WSGIPassAuthorization On
    <Directory $api_dir/config/>
        <Files wsgi.py>
            Require all granted
        </Files>
    </Directory>
    <Directory /usr/local/lib/python3.6/dist-packages/django/contrib/admin/static/admin/>
        Require all granted
    </Directory>
    <Directory /usr/local/lib/python3.6/dist-packages/rest_framework/static/rest_framework/>
        Require all granted
    </Directory>
    <Directory /usr/local/lib/python3.6/dist-packages/debug_toolbar/static/debug_toolbar/>
        Require all granted
    </Directory>
    <Directory /home/site/api/storage/collect_static/>
        Require all granted
     </Directory>
</VirtualHost>
"
