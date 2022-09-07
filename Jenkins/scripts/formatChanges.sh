changes=$1
changes=$(echo $changes | xargs awk -F "/" '{print $1}' | tr '\n' '-')
echo $changes