# Variables (for Jenkins)
variable "access_key"                   {}
variable "secret_key"                   {}
variable "service"                      {}
variable "ami"                          {}
variable "instance_type"                {}
variable "sec_group"					{}
variable "vpc_id"                       {}
variable "subnets" 						{}
variable "owner"                        { default = "DevOps" }

# for DNS record
variable "gettio_zone_id"               { default = "ZXXXXXXXXXXXX5G" }
variable "hostname"                     {}


terraform {
  backend "s3" {
    bucket = "vvvv-terraform"
    key    = "terraform-infra/dev/infra/raise_instance/terraform.tfstate"
    region = "eu-west-1"
  }
}