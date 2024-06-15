#!/bin/bash
#应用于DO374动态主机清单教学
# 处理--list参数
list() {
    cat << EOF
{
    "_meta": {
        "hostvars": {}
    },
    "webservers": {
        "hosts": ["web01", "web02"],
        "vars": {
            "webpkgs": "apache"
        }
    },
    "dbservers": {
        "hosts": ["db01.example.com", "db02.example.com"]
    },
    "all": {
        "children": ["webservers", "dbservers"],
        "hosts": ["test1", "test2", "test3", "test4", "test5"]
    }
}
EOF
}

# 处理--host参数
host() {
    hostname=$1
    case $hostname in
        web01 | web02)
            echo '{"ansible_connection": "ssh", "ansible_host": "'$hostname'"}'
            ;;
        db01.example.com | db02.example.com)
            echo '{"ansible_connection": "ssh", "ansible_host": "'$hostname'"}'
            ;;
        test*)
            echo '{"ansible_connection": "ssh", "ansible_host": "'$hostname'"}'
            ;;
        *)
            echo "{}"
            ;;
    esac
}

# 根据参数调用相应的函数
case $1 in
    --list)
        list
        ;;
    --host)
        host $2
        ;;
    *)
        echo "Usage: $0 --list|--host <hostname>"
        ;;
esac
