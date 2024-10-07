#!/bin/sh
proto_dir="simple_waymo_open_dataset_reader"

protoc -I=. --python_out=. $proto_dir/label.proto
protoc -I=. --python_out=. $proto_dir/dataset.proto
protoc -I=. --python_out=. $proto_dir/map.proto
protoc -I=. --python_out=. $proto_dir/camera_tokens.proto
protoc -I=. --python_out=. $proto_dir/compressed_lidar.proto
protoc -I=. --python_out=. $proto_dir/scenario.proto