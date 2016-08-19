from kazoo.client import KazooClient
import kazoo
import time
zk = KazooClient(hosts='172.30.63.169:2181')
zk.start()
#zk.create("/testzoo",value=b"head",makepath=True)

def ensureBasicStructure():
    zk.ensure_path("/testzoo")
    zk.ensure_path("/testzoo/hosts")
    zk.ensure_path("/testzoo/hosts/all")
    zk.ensure_path("/testzoo/hosts/alive")
    zk.ensure_path("/testzoo/hosts/down")

def createNodeinAll():
    try:
        zk.create("/testzoo/hosts/all/client2")
        zk.create("/testzoo/hosts/alive/client2", b"a value", None, True)
    except kazoo.exceptions.NodeExistsError:
        print("Node all ready created")

def leaderCheck():
    asd=zk.command(b"stat")
    node_state=[x.replace("Mode: ","") for x in asd.split('\n') if x.startswith('Mode:')][0]
    return (node_state)
def leaderCheck1():
    asd=zk.command(b"stat")
    node_state=[x.replace("Mode: ","") for x in asd.split('\n') if x.startswith('Mode:')][0]
    return (node_state)


def createNode():
    if(zk.exists("/testzoo/hosts/all/client2")):
        print()
    else:
        try:
            zk.create("/testzoo/hosts/all/client2")
        except:
            print("node already their...!")

    if(zk.exists("/testzoo/hosts/alive/client2")):
        print()
    else:
        try:
            zk.create("/testzoo/hosts/alive/client2", b"a value", None, True)
        except:
            print("Node already their...!")
    if(zk.ensure_path("/testzoo/hosts/down/client2")):
            zk.delete("/testzoo/hosts/down/client2",recursive=True)
    else:
        create = createNodeinAll()


ensureing=ensureBasicStructure()
down=createNode()


while 1:
    leader = leaderCheck()
    print("indide the loop...!!")
    if (leader=="leader"):
        print("i'm leader host...168")
        all=zk.get_children("/testzoo/hosts/all")
        alive=zk.get_children("/testzoo/hosts/alive")
        down=zk.get_children("/testzoo/hosts/down")
        if(all==(alive+down)):
            print ("No operation....!")
        else:
            print("add the down node to Down path..!")
            down_Node=tem=list(set(all) - set(alive))
            print(down_Node)
            for node in down_Node:
                try:
                    zk.create("/testzoo/hosts/down/" + node, b"a value", None, True)
                except:
                    print("down node already present...!" + node)

                    #zk.stop()
