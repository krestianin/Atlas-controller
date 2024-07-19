#!/bin/bash
echo '{"id":0,"jsonrpc":"2.0","cmd":"get_error_code"}' | netcat $1 $2 -q1 -w10