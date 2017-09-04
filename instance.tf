provider "aws" {
  access_key = "${var.access_key}"
  secret_key = "${var.secret_key}"
  region = "eu-west-1"
}


data "template_file" "userdata" {
  template = "${file("userdata-instance.txt")}"
  vars {service = "${var.service}-test"}
}


resource "random_shuffle" "subnets" {
  input = ["${split(",", var.subnets)}"]
  result_count = 1
}


# Test instance
resource "aws_instance" "instance" {
  ami = "${var.ami}"
  instance_type = "${var.instance_type}"
  key_name = "xxxxxxxxxxxx"
  iam_instance_profile = "s3_chef_reader"
  associate_public_ip_address = false
  vpc_security_group_ids = ["${var.sec_group}"]
  user_data = "${data.template_file.userdata.rendered}"
  subnet_id = "${random_shuffle.subnets.result[0]}"
  associate_public_ip_address = true
  tags {
    Name="${var.service}-test"
    owner = "${var.owner}"
    stackdriver_monitor="false"
  }
}

# DNS record
resource "aws_route53_record" "vvvvio" {
  zone_id = "${var.vvvvio_zone_id}"
  name = "${var.service}-test"
  type = "A"
  ttl     = "60"
  records = ["${aws_instance.instance.private_ip}"]
}
