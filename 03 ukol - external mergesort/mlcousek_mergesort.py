import random
import os
import heapq
import sys


def generate_number_file(file_name, num_lines, min_value=0, max_value=100000000):
     with open(file_name, 'w') as f:
        for _ in range(num_lines):
            number = random.randint(min_value, max_value)
            f.write(f"{number}\n")


def split_file(input_file, chunk_size, output_prefix):
    """Rozdělí vstupní soubor na menší chunky."""
    chunk_files = []
    with open(input_file, 'r') as infile:
        chunk = []
        for line in infile:
            chunk.append(int(line.strip()))
            if len(chunk) * 40 >= chunk_size:  # TADY TA 40 JE KONSTANTA 
                chunk.sort()
                chunk_file = f"{output_prefix}_chunk_{len(chunk_files)}.txt"
                with open(chunk_file, 'w') as cf:
                    cf.write("\n".join(map(str, chunk)) + "\n")
                chunk_files.append(chunk_file)
                chunk = []
        if chunk:
            chunk.sort()
            chunk_file = f"{output_prefix}_chunk_{len(chunk_files)}.txt"
            with open(chunk_file, 'w') as cf:
                cf.write("\n".join(map(str, chunk)) + "\n")
            chunk_files.append(chunk_file)
    return chunk_files


def merge_chunks(chunk_files, output_file, block_size):
    """Sloučí seřazené chunky do jednoho výstupního souboru."""
    min_heap = []
    file_handles = [open(f, 'r') for f in chunk_files]
    
    
    ##num_files = len(chunk_files)
    ##values_per_file = block_size // num_files // 8
    
    
    ##blocks = []
    
    ##for i, fh in enumerate(file_handles):
      ##  block = []
        
       ## for _ in range(values_per_file):
         ##   line = fh.readline()            ### MEL JSEM TO IMLEMENTOVANE POMOCI BLOKU, ALE NEDOKAZAL JSEM TO UDELAT TAK ABY TO NA 100MB PAMETI JELO (TAK JSEM TO ZACAL NACITAT PO RADCICH)
           ## if not line:
             ##   break  # Konec souboru
            ##block.append(int(line.strip()))
            
            
       ## if block:
         ##   block.sort()
           ## heapq.heappush(min_heap, (block[0], i, 0, block))
            ##blocks.append((block, i))   
        
  
    for i, fh in enumerate(file_handles):
        line = fh.readline()
        if line:
            heapq.heappush(min_heap, (int(line.strip()), i))
            
    with open(output_file, 'w') as outfile:
        # Iterativně vybírej nejmenší čísla z haldy
        while min_heap:
            smallest, file_index = heapq.heappop(min_heap)
            outfile.write(f"{smallest}\n")  # Zapiš nejmenší číslo do výstupu

            # Načti další číslo ze stejného souboru
            next_line = file_handles[file_index].readline()
            if next_line:  # Pokud soubor není prázdný
                heapq.heappush(min_heap, (int(next_line.strip()), file_index))
    
    """       
    with open(output_file, 'w') as outfile:
 
        while min_heap:
            
                
            smallest, index, idx_in_block, block = heapq.heappop(min_heap)
            outfile.write(f"{smallest}\n")
            
            # Pokud máme další číslo v tomto bloku, přidáme ho do haldy
            if idx_in_block + 1 < len(block):
                heapq.heappush(min_heap, (block[idx_in_block + 1], index, idx_in_block + 1, block)) #PRACE S BLOKAMA
            else:
                block = []
                for _ in range(values_per_file):
                    line = file_handles[index].readline()
                    if not line:
                        break  # Konec souboru
                    block.append(int(line.strip()))
                
                if block:
                    block.sort()
                    heapq.heappush(min_heap, (block[0], index, 0, block))
                    blocks.append((block, i))
    """                           
    for fh in file_handles:
        fh.close()
        
    #MAZANI
    for f in chunk_files: #TADY KDYZTAK ODKOMENTOVAT PRO SMAZANI TEMP SOUBORU
      os.remove(f)


def external_mergesort(input_file, output_file, memory_limit, block_size):
    """Implementace externího mergesortu."""
    chunk_size = memory_limit // 4  # Rozumný limit pro velikost chunku
    chunk_files = split_file(input_file, chunk_size, "temp")
    merge_chunks(chunk_files, output_file, block_size)


if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("Použití: python prijmeni_mergesort.py vstupni_soubor")
        sys.exit(1)
  
        
    file_name = "input_numbers.txt"  # Název výstupního souboru
    num_lines = 20_000_000  # Počet generovaných čísel
    min_value = 0       # Minimální hodnota
    max_value = 100_000_000 # Maximální hodnota ####taky se podle tohoto meni velikost souboru 
    


#VYGENEROVANI SOUBORU
   
    #generate_number_file(file_name, num_lines, min_value, max_value)
    #print(f"Soubor '{file_name}' byl vytvoren s {num_lines} cisly.")
    
    

    input_file = sys.argv[1]
    #input_file = "input_numbers.txt"
    output_file = "output.txt"
    memory_limit = 100 * 1024 * 1024  # 100 MB
    block_size = 128  # 512 B

    external_mergesort(input_file, output_file, memory_limit, block_size)
    print(f"Serazeny soubor byl ulozen do {output_file}.")
    
