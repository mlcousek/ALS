class Node:
    def __init__(self, hashValue):
        self.hashValue = hashValue
        self.resources = {}
        self.next = None
        self.previous = None
        self.fingerTable = {}


class HashRing:
    def __init__(self, k):
        self.head = None
        self.k = k
        self.min = 0
        self.max = 2**k - 1

    def legalRange(self, hashValue):
        return self.min <= hashValue <= self.max

    def distance(self, a, b):
        if a == b:
            return 0
        elif a < b:
            return b - a
        else:
            return (2**self.k) + (b - a)

    def lookupNode(self, hashValue):
        if self.legalRange(hashValue):
            temp = self.head
            if temp is None:
                return None
            else:
                while(self.distance(temp.hashValue, hashValue) >
                        self.distance(temp.next.hashValue, hashValue)):
                    temp = temp.next
                if temp.hashValue == hashValue:
                    return temp
                return temp.next

    def moveResources(self, dest, orig, deleteTrue):
        delete_list = []
        for i, j in orig.resources.items():
            if (self.distance(i, dest.hashValue) < self.distance(i, orig.hashValue) or deleteTrue):
                dest.resources[i] = j
                delete_list.append(i)
                print("\tMoving a resource " + str(i) + " from " +
                      str(orig.hashValue) + " to " + str(dest.hashValue))
        for i in delete_list:
            del orig.resources[i]


    def addNode(self, hashValue):
        if self.legalRange(hashValue):
            newNode = Node(hashValue)

            if self.head is None:
                newNode.next = newNode
                newNode.previous = newNode
                self.head = newNode
                print("Adding a head node " + str(newNode.hashValue) + "...")
            else:
                temp = self.lookupNode(hashValue)
                newNode.next = temp
                newNode.previous = temp.previous
                newNode.previous.next = newNode
                newNode.next.previous = newNode
                print("Adding a node " + str(newNode.hashValue) +
                      ". Its prev is " + str(newNode.previous.hashValue) +
                      ", and its next is " + str(newNode.next.hashValue) + ".")

                self.moveResources(newNode, newNode.next, False)

                if hashValue < self.head.hashValue:
                    self.head = newNode

    def addResource(self, hashValueResource):
        if self.legalRange(hashValueResource):
            print("Adding a resource " + str(hashValueResource) + "...")
            targetNode = self.lookupNode(hashValueResource)
            if targetNode is not None:
                value = "Dummy resource value of " + str(hashValueResource)
                targetNode.resources[hashValueResource] = value
            else:
                print("Can't add a resource to an empty hashring")

    def removeNode(self, hashValue):
        temp = self.lookupNode(hashValue)
        if temp.hashValue == hashValue:
            print("Removing the node " + str(hashValue) + ": ")
            self.moveResources(temp.next, temp, True)
            temp.previous.next = temp.next
            temp.next.previous = temp.previous
            if self.head.hashValue == hashValue:
                self.head = temp.next
                if self.head == self.head.next:
                    self.head = None
            return temp.next
        else:
            print("Nothing to remove.")


    def printHashRing(self):
        print("*****")
        print("Printing the hashring in clockwise order:")
        temp = self.head
        if self.head is None:
            print("Empty hashring")
        else:
            while(True):
                print("Node: " + str(temp.hashValue) + ", ", end=" ")

                print("Resources: ", end=" ")
                if not bool(temp.resources):
                    print("Empty", end="")
                else:
                    for i in temp.resources.keys():
                        print(str(i), end=" ")

                temp = temp.next
                print(" ")
                if (temp == self.head):
                    break
        print("*****")
    
    def buildFingerTables(self):
        print("Building finger tables for each node...")
        if self.head is None:
            return

        temp = self.head
        while True:
            for i in range(self.k):  
                finger_hash = (temp.hashValue + 2**i) % (2**self.k)
                successor = self.lookupNode(finger_hash)
                temp.fingerTable[i] = successor
                print(f"Node {temp.hashValue} -> Finger {i} points to Node {successor.hashValue}")
            temp = temp.next
            if temp == self.head:
                break


    def chordLookup(self, hashValue):
        if self.head is None:
            return None

        temp = self.head
        while temp:
            # Zkontrolujeme, zda má uzel hashValue, pokud ano, vrátíme jej
            if temp.hashValue == hashValue:
                return temp

            # Projdeme finger tabulku a hledáme nejbližší finger před hashValue
            closest_finger = temp
            for i in range(self.k - 1, -1, -1):  # procházíme od nejvzdálenějšího
                if self.distance(temp.fingerTable[i].hashValue, hashValue) < self.distance(closest_finger.hashValue, hashValue):
                    closest_finger = temp.fingerTable[i]

            #print(temp)
            # Pokud jsme našli uzel s hashValue, vrátíme ho
            if closest_finger.hashValue == hashValue:
                return closest_finger
            elif closest_finger == temp:
                return temp.next  # pokud není finger blíže, přejdeme na následující uzel
            else:
                temp = closest_finger  # pokračujeme hledáním od nejlepšího fingeru
    
    def chordLookupWithSteps(self, hashValue):
        steps = 0  # počítadlo kroků
        if self.head is None:
            return None, steps  # pokud není žádný uzel, vrátí počet kroků 0

        temp = self.head
        while temp:
            steps += 1  # navštívení uzlu

            # Zkontrolujeme, zda má uzel hashValue, pokud ano, vrátíme jej
            if temp.hashValue == hashValue:
                return temp, steps

            # Projdeme finger tabulku a hledáme nejbližší finger před hashValue
            closest_finger = temp
            for i in range(self.k - 1, -1, -1):  # procházíme od nejvzdálenějšího
                if self.distance(temp.fingerTable[i].hashValue, hashValue) < self.distance(closest_finger.hashValue, hashValue):
                    closest_finger = temp.fingerTable[i]

            # Pokud jsme našli uzel s hashValue, vrátíme ho
            if closest_finger.hashValue == hashValue:
                return closest_finger, steps + 1  # +1 pro návštěvu closest_finger
            elif closest_finger == temp:
                # pokud není finger blíže, přejdeme na následující uzel
                return temp.next, steps + 1
            else:
                # pokračujeme hledáním od nejlepšího fingeru
                temp = closest_finger

        return None, steps  # pokud nebyl nalezen, vrátí None a počet kroků



"""
if __name__ == '__main__':
    hr = HashRing(5)
    print(hr.distance(29, 5))
    print(hr.distance(29, 12))
    print(hr.distance(5, 29))
    print(hr.distance(43, 12))
"""

if __name__ == '__main__':
    hr = HashRing(5)
    hr.addNode(12)
    hr.addNode(18)
    hr.addResource(24)
    hr.addResource(21)
    hr.addResource(16)
    hr.addResource(23)
    hr.addResource(2)
    hr.addResource(29)
    hr.addResource(28)
    hr.addResource(7)
    hr.addResource(10)
    hr.printHashRing()

    hr.addNode(5)
    hr.addNode(27)
    hr.addNode(30)
    hr.printHashRing()

    hr.removeNode(12)
    hr.buildFingerTables()
    hr.printHashRing()

    x, s = hr.chordLookupWithSteps(31)
    x2 = hr.lookupNode(31)
    print(x.hashValue)
    print(s)
    print(x2.hashValue)
    
