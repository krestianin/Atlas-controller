#!/bin/bash
echo '{"id":0,"jsonrpc":"2.0","command":"devs"}' | netcat $1 $2 -q1 -w10 -N