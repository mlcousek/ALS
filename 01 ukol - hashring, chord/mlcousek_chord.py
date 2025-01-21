import mmh3
import sys

class Node:
    def __init__(self, hashValue, name):
        self.hashValue = hashValue
        self.resources = {}
        self.next = None
        self.previous = None
        self.name = name
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

    def lookupNodeWithSteps(self, hashValue):
        steps = 0  
        if self.legalRange(hashValue):
            temp = self.head
            if temp is None:
                return None, steps 
            else:
                steps += 1  
                if hashValue in temp.resources:
                    return temp, steps
                while self.distance(temp.hashValue, hashValue) > self.distance(temp.next.hashValue, hashValue):
                    temp = temp.next
                    steps += 1  
                if temp.hashValue == hashValue:
                    if hashValue not in temp.resources:
                        return None, steps
                    else:
                        return temp, steps
                if hashValue not in temp.next.resources:
                    return None, steps
                else:
                    return temp.next, steps + 1  
        return None, steps

    def lookupServer(self, hashValue):
        if self.legalRange(hashValue):
            temp = self.head
            if temp is None:
                return None
            elif temp.hashValue == hashValue:
                return temp
            else:
                temp = temp.next
                while(self.head.hashValue != temp.hashValue):
                    if temp.hashValue == hashValue:
                        return temp
                    temp = temp.next
                return None

    def moveResources(self, dest, orig, deleteTrue):
        delete_list = []
        for i, j in orig.resources.items():
            if (self.distance(i, dest.hashValue) < self.distance(i, orig.hashValue) or deleteTrue):
                dest.resources[i] = j
                delete_list.append(i)
        for i in delete_list:
            del orig.resources[i]


    def addNode(self, hashValue, name):
        if self.legalRange(hashValue):
            node = self.lookupServer(hashValue)
            if node is None:
                newNode = Node(hashValue, name)

                if self.head is None:
                    newNode.next = newNode
                    newNode.previous = newNode
                    self.head = newNode
                else:
                    temp = self.lookupNode(hashValue)
                    newNode.next = temp
                    newNode.previous = temp.previous
                    newNode.previous.next = newNode
                    newNode.next.previous = newNode
                    
                    self.moveResources(newNode, newNode.next, False)

                    if hashValue < self.head.hashValue:
                        self.head = newNode
                self.buildFingerTables()
                return newNode
            else:
                return None

    def addResource(self, hashValueResource, name):
        if self.head is None:
            return None
        else:
            if self.legalRange(hashValueResource):
                targetNode = self.lookupNode(hashValueResource)
                if targetNode is not None:
                    targetNode.resources[hashValueResource] = name
                return targetNode

    def removeNode(self, hashValue):
        temp = self.lookupNode(hashValue)
        if temp is not None:
            if temp.hashValue == hashValue:
                self.moveResources(temp.next, temp, True)
                temp.previous.next = temp.next
                temp.next.previous = temp.previous
                if self.head.hashValue == hashValue:
                    if self.head == self.head.next:
                        self.head = None
                    else:
                        self.head = temp.next
                self.buildFingerTables()
                return temp.next
            else:
                return None
        else:
            return None

    def printHashRing(self):
        print("*****")
        print("Printing the hashring in clockwise order:")
        temp = self.head
        if self.head is None:
            print("Empty hashring")
        else:
            while(True):
                print(f"Node: {temp.name} (hash {temp.hashValue}), Resources:", end=" ")

                if not bool(temp.resources):
                    print("Empty", end="")
                else:
                    for resource_hash, resource_name in temp.resources.items():
                        print(f"{resource_name} (hash {resource_hash})", end=" ")

                temp = temp.next
                print(" ")
                if (temp == self.head):
                    break
        print("*****")
    
    def buildFingerTables(self):
        if self.head is None:
            return

        temp = self.head
        while True:
            for i in range(self.k):  
                finger_hash = (temp.hashValue + 2**i) % (2**self.k)
                successor = self.lookupNode(finger_hash)
                temp.fingerTable[i] = successor
            temp = temp.next
            if temp == self.head:
                break

# ChordLookup - zde je implementace metody pro vyhledání stránky v Chordu i stranek co tam nejsou
    def chordLookup(self, hashValue):
        if self.head is None:
            return None
        temp = self.head
        while temp:
            if temp.hashValue == hashValue:
                return temp

            closest_finger = temp
            for i in range(self.k - 1, -1, -1):  # procházíme od nejvzdálenějšího
                if self.distance(temp.fingerTable[i].hashValue, hashValue) < self.distance(closest_finger.hashValue, hashValue):
                    closest_finger = temp.fingerTable[i]

            if closest_finger.hashValue == hashValue:
                return closest_finger
            elif closest_finger == temp:
                return temp.next  # pokud není finger blíže, přejdeme na následující uzel
            else:
                temp = closest_finger  # pokračujeme hledáním od nejlepšího fingeru

# ChordLookupWithSteps - zde je implementace metody pro vyhledání stránky v Chordu jen strancek co tam jsou a u toho pocita i kroky
    def chordLookupWithSteps(self, hashValue):
        steps = 0  
        if self.head is None:
            return None, steps  

        temp = self.head
        
        if hashValue in temp.resources:
            steps += 1
            return temp, steps
        
        while temp:
            steps += 1  
            if temp.hashValue == hashValue:
                if hashValue in temp.resources:
                    return temp, steps
                else:
                    return None, steps
            closest_finger = temp
            for i in range(self.k - 1, -1, -1):  # procházíme od nejvzdálenějšího
                if self.distance(temp.fingerTable[i].hashValue, hashValue) < self.distance(closest_finger.hashValue, hashValue):
                    closest_finger = temp.fingerTable[i]

            if closest_finger.hashValue == hashValue:
                if hashValue in closest_finger.resources:
                    return closest_finger, steps + 1
                else:
                    return None, steps + 1
            elif closest_finger == temp:
                if hashValue in temp.next.resources:
                    return temp.next, steps + 1
                else:
                    return None, steps + 1
            else:
                temp = closest_finger
        return None, steps  

def load_data(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

# Program
def main(servers_file, pages_file):

    hr = HashRing(32)
    
    servers = load_data(servers_file)
    pages = load_data(pages_file)
    
    for server in servers:
        hash_value = mmh3.hash(server, 0, False)
        hr.addNode(hash_value, server)
    
    for page in pages:
        hash_value = mmh3.hash(page, 0, False)
        hr.addResource(hash_value, page)
   
    while True:
        print("\nVyberte možnost:")
        print("a) Vypsat chord (jména stránek na serverech)")
        print("b) Přidat server")
        print("c) Odebrat server")
        print("d) Přidat stránku")
        print("e) Vyhledat stránku v hashringu")
        print("f) Vyhledat stránku v chord")
        print("x) Konec")
        
        choice = input("Zadejte volbu: ").strip().lower()
        
        if choice == 'a':
            hr.printHashRing()
        elif choice == 'b':
            server_name = input("Zadejte jméno serveru: ").strip()
            hash_value = mmh3.hash(server_name, 0, False)
            x = hr.addNode(hash_value, server_name)
            if x == None:
                print(f"Server {server_name} již existuje.")
        elif choice == 'c':
            server_name = input("Zadejte jméno serveru k odebrání: ").strip()
            hash_value = mmh3.hash(server_name, 0, False)
            x = hr.removeNode(hash_value)
            if x == None:
                print(f"Server {server_name} nebyl nalezen.")
        elif choice == 'd':
            page_name = input("Zadejte jméno stránky: ").strip()
            hash_value = mmh3.hash(page_name, 0, False)
            x = hr.addResource(hash_value, page_name)
            if x == None:
                print(f"Neexistuje zadny server.")
        elif choice == 'e':
            page_name = input("Zadejte jméno stránky k vyhledání: ").strip()
            hash_value = mmh3.hash(page_name, 0, False)
            node, steps = hr.lookupNodeWithSteps(hash_value)
            if(node == None):
                print(f"Stránka {page_name} nebyla nalezena (kroky: {steps})")
            else:
                print(f"Stránka {page_name} je uložena na serveru {node.name} (kroky: {steps})")
        elif choice == 'f':
            page_name = input("Zadejte jméno stránky k vyhledání: ").strip()
            hash_value = mmh3.hash(page_name, 0, False)
            hr.buildFingerTables()
            node, steps = hr.chordLookupWithSteps(hash_value)
            if(node == None):
                print(f"Stránka {page_name} nebyla nalezena (kroky: {steps})")
            else:
                print(f"Stránka {page_name} je uložena na serveru {node.name} (kroky: {steps})")
        elif choice == 'x':
            print("Konec programu.")
            break
        else:
            print("Neplatná volba, zkuste to znovu.")



if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Použití: python3 prijmeni_chord.py servery.txt stranky.txt")
    else:
        main(sys.argv[1], sys.argv[2])
    

        
        
        
        
        
