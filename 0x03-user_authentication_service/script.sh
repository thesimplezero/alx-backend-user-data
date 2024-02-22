#!/bin/bash

# Define colors
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Test 1: Register a new user
response=$(curl -s -o /dev/null -w "%{http_code}" -XPOST localhost:5000/users -d 'email=bob@me.com' -d 'password=mySuperPwd')
if [ "$response" -eq 200 ]; then
    echo -e "${GREEN}Test 1 passed${NC}"
else
    echo -e "${RED}Test 1 failed${NC}"
fi

# Test 2: Try to register the same user again
response=$(curl -s -o /dev/null -w "%{http_code}" -XPOST localhost:5000/users -d 'email=bob@me.com' -d 'password=mySuperPwd')
if [ "$response" -eq 400 ]; then
    echo -e "${GREEN}Test 2 passed${NC}"
else
    echo -e "${RED}Test 2 failed${NC}"
fi
