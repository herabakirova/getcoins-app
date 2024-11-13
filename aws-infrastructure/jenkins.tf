data "aws_ami" "amazon_ami" {
  most_recent = true
  owners      = ["amazon"]
  filter {
    name   = "name"
    values = ["al2023-ami-2023.*-x86_64"]
  }
  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

resource "aws_key_pair" "public_key" {
  key_name   = var.key_name
  public_key = file(var.path_to_public_key)
}

resource "aws_instance" "jenkins" {
  ami             = data.aws_ami.amazon_ami.id
  instance_type   = var.instance_type
  subnet_id       = aws_subnet.first_subnet.id
  vpc_security_group_ids = [aws_security_group.sec_group.id]
  key_name        = aws_key_pair.public_key.key_name
  user_data       = file("${path.module}/userdata.sh")

  tags = {
    Name = var.jenkins_name
  }
}

resource "null_resource" "wait_for_jenkins" {
  provisioner "local-exec" {
    command = <<EOT
      for i in {1..10}; do
        ssh -o StrictHostKeyChecking=no -i ${var.path_to_private_key} ec2-user@${aws_instance.jenkins.public_ip} "sudo cat /var/lib/jenkins/secrets/initialAdminPassword" && break || sleep 30
      done
    EOT
  }

  depends_on = [aws_instance.jenkins]
}
