from troposphere import Ref, Template, Parameter, Output, Join, GetAtt, Base64
import troposphere.ec2 as ec2
from troposphere.iam import InstanceProfile, PolicyType as IAMPolicy, Role
from awacs.aws import Action, Allow, Policy, Principal, Statement
from awacs.sts import AssumeRole
t = Template()

#Sec Group
#AMI
#SSH Key Pair

sg = ec2.SecurityGroup("LampSg")
sg.GroupDescription = "Allow acccess through ports 80 and 22 through web server"
sg.SecurityGroupIngress = [
    ec2.SecurityGroupRule(IpProtocol = "tcp", FromPort = "22", ToPort = "22", CidrIp = "0.0.0.0/0"),
    ec2.SecurityGroupRule(IpProtocol = "tcp", FromPort = "80", ToPort = "80", CidrIp = "0.0.0.0/0")
]

t.add_resource(sg)

keypair = t.add_parameter(Parameter(
    "KeyName",
    Description = "Name of the SSH Key Pair that will be used",
    Type="String"
))

instance = ec2.Instance("LampStage")
instance.ImageId = "ami-08d489468314a58df"
instance.InstanceType="t2.micro"
instance.SecurityGroups=[Ref(sg)]
instance.KeyName = Ref(keypair)

principale = Principal("Service", ["ec2.amazonaws.com"])
statement = Statement(Effect=Allow, Action=[AssumeRole], Principal=principale)
policy = Policy(Statement=[statement])
role = Role("Role", AssumeRolePolicyDocument=policy)

t.add_resource(role)

t.add_resource(InstanceProfile("InstanceProfile", Path="/", Roles=[Ref("Role")]))

t.add_resource(IAMPolicy("Policy",PolicyName="AllowS3",PolicyDocument=Policy(Statement=[Statement(Effect=Allow,Action=[Action("s3","*")],Resource=["*"])]),Roles=[Ref("Role")]))

t.add_resource(instance)

t.add_output(Output(
    "InstanceAccess",
    Description = "Command to use to access the instance using SSH",
    Value = Join("",["ssh -i /Users/ajayshenoy/projects/aws_certificate_course/DevOps/LampKey.pem ec2-user@", GetAtt(instance, "PublicDnsName")])
))

t.add_output(Output(
    "WebUrl",
    Description = "The URL of the web server",
    Value = Join("",["http://", GetAtt(instance, "PublicDnsName")])
))
print(t.to_json())