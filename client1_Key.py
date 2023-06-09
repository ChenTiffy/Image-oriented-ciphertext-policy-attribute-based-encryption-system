from charm.toolbox.pairinggroup import PairingGroup,GT

from charm.toolbox.pairinggroup import PairingGroup

from client1_abenc import CPabe_BSW07



def keyGen(access_policy, pk):

    groupObj = PairingGroup('SS512')

    cpabe = CPabe_BSW07(groupObj)

    rand_msg = groupObj.random(GT)

    #加密图像的密钥

    str_key = str(rand_msg)

    key1 = ord(str_key[1])

    key2 = ord(str_key[2])



    #加密密钥



    ct = cpabe.encrypt(pk, rand_msg, access_policy)



    return key1, key2, ct, rand_msg