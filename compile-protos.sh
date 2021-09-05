#!/usr/bin/env bash

protoc -I protos/ protos/authentication.proto --python_out=app/domain/authorization