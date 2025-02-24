
import sys

class Folder:
    def __init__(self, name, parent = None):
        self.name = name
        self.parent = parent
        self.folders = {}
    
    def get_name(self):
        return self.name
    
    def get_parent(self):
        return self.parent
    
    def add_folder(self, folder):
        self.folders[folder.get_name()] = folder
    
    def get_folders(self):
        return self.folders
    
    def list_hierarchy(self, level = 0):
        print(" " * level + self.name)
        level += 1
        for folder in self.folders:
            self.folders[folder].list_hierarchy(level)


class InstructionsParser:
    def __init__(self, filename):
        self.filename = filename
    
    def get_file_name(self):
        return self.filename
    
    def parse(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            self.instructions = []
            for line in lines:
                self.instructions.append(line.strip())
        return self.instructions
    
    def create(self, folders, folder_hierarchies):
        parent = None
        root = folder_hierarchies.get(folders[0], None)
        for folder in folders:
            if root == None:
                new_folder = Folder(folder)
                folder_hierarchies[folder] = new_folder
                parent = new_folder
            elif parent and folder not in parent.get_folders().keys():
                new_folder = Folder(folder, parent)
                parent.add_folder(new_folder)
                parent = new_folder
            elif parent and folder in parent.get_folders().keys():
                parent = parent.get_folders()[folder]
            else:
                parent = root
    
    def delete(self, folders, folder_hierarchies):
        root = folder_hierarchies.get(folders[0], None)
        if not root:
                print(f"Cannot delete {split_instruction[1]} - {folders[0]} does not exist")
        else:
            for folder in folders[1:]:
                if not root:
                    print(f"Cannot delete {split_instruction[1]} - {folder} does not exist")
                    break
                root = root.get_folders().get(folder, None)
            if root:
                parent = root.get_parent()
                parent.get_folders().pop(root.get_name())
    
    def move(self, folders, folder_hierarchies, destination):
        root = folder_hierarchies.get(folders[0], None)
        if not root:
                print(f"Cannot move {split_instruction[1]} - {folder} does not exist")
        else:
            for folder in folders[1:]:
                if not root:
                    print(f"Cannot move {split_instruction[1]} - {folder} does not exist")
                    break
                root = root.get_folders().get(folder, None)
            if root:
                parent = root.get_parent()
                if parent:
                    parent.get_folders().pop(root.get_name())
                else:
                    folder_hierarchies.pop(root.get_name())
                destination_root = folder_hierarchies.get(destination[0], None)
                for folder in destination[1:]:
                    if not destination_root:
                        print(f"Cannot move {split_instruction[1]} - {folder} does not exist")
                        break
                    destination_root = destination_root.get_folders().get(folder, None)
                if destination_root:
                    destination_root.add_folder(root)
                else:
                    print(f"Cannot move {split_instruction[1]} - {destination[-1]} does not exist")
    
    def list(self, folder_hierarchies):
        for folder in folder_hierarchies.values():
            folder.list_hierarchy()
    
if __name__ == "__main__":
    parser = InstructionsParser(sys.argv[-1])
    instructions = None
    try:
        instructions = parser.parse()
    except:
        print(f"Instructions file: \"{sys.argv[-1]}\" not found")
        sys.exit(1)

    folder_hierarchies = {}
    for instruction in instructions:
        print(instruction)
        split_instruction = instruction.split(' ')
        if split_instruction[0] == 'CREATE':
            folders = split_instruction[1].split('/')
            parser.create(folders, folder_hierarchies)
        elif split_instruction[0] == 'DELETE':
            folders = split_instruction[1].split('/')
            parser.delete(folders, folder_hierarchies)
        elif split_instruction[0] == 'MOVE':
            folders = split_instruction[1].split('/')
            destination = split_instruction[2].split('/')
            parser.move(folders, folder_hierarchies, destination)
        elif split_instruction[0] == 'LIST':
            parser.list(folder_hierarchies)