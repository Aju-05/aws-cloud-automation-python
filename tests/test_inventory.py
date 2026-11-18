from scripts.ec2_inventory import instance_name


def test_instance_name_returns_name_tag():
    assert instance_name([{"Key": "Name", "Value": "api-node"}]) == "api-node"


def test_instance_name_returns_empty_when_missing():
    assert instance_name([{"Key": "Environment", "Value": "dev"}]) == ""
    assert instance_name(None) == ""
