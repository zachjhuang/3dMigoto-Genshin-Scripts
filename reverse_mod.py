import os
import struct

class Mod:
    def __init__(self) -> None:
        self.mod_name = ''
        self.hashes = {}
        self.first_indices = {}
        self.strides = {}
        self.formats = {}
        for _, _, files in os.walk('.'):
            for file in files:
                if '.ini' in file and 'desktop' not in file:
                    self.ini = file
    
    def parse_ini_line(self, keyword, line, component, dict):
        if keyword in line:
            dict[component] = line.split('=')[1].strip()

    def parse_ini(self) -> None:
        print("Parsing .ini file...")
        with open(self.ini, 'r') as ini:
            current_component = ''
            for line in ini:
                line = line.strip()
                if '[TextureOverride' + self.mod_name in line or '[Resource' + self.mod_name in line:
                    if self.mod_name == '':
                        self.mod_name = line.split('[TextureOverride')[1].split('Position]')[0]
                    current_component = line.split(self.mod_name)[1].split(']')[0]
                self.parse_ini_line('hash', line, current_component, self.hashes)
                self.parse_ini_line('match_first_index', line, current_component, self.first_indices)
                self.parse_ini_line('stride', line, current_component, self.strides)
                self.parse_ini_line('format', line, current_component, self.formats)

    def parse_buffers(self):
        print("Parsing .buf files...")
        with open(f'{self.mod_name}Position.buf', 'rb') as f:
            position_data = f.read()
        with open(f'{self.mod_name}Blend.buf', 'rb') as f:
            blend_data = f.read()
        with open(f'{self.mod_name}Texcoord.buf', 'rb') as f:
            texcoord_data = f.read()

        self.vertex_count = len(position_data) // int(self.strides["Position"])
        self.vb = [{} for _ in range(self.vertex_count)]

        for i in range(self.vertex_count):
            n = int(self.strides["Position"])
            self.vb[i]["POSITION"] = [struct.unpack('<f', position_data[n*i+4*j : n*i+4*(j+1)])[0] for j in range(3)]
            self.vb[i]["NORMAL"] = [struct.unpack('<f', position_data[n*i+12+4*j : n*i+12+4*(j+1)])[0] for j in range(3)]
            self.vb[i]["TANGENT"] = [struct.unpack('<f', position_data[n*i+24+4*j : n*i+24+4*(j+1)])[0] for j in range(4)]

            n = int(self.strides["Blend"])
            self.vb[i]["BLENDWEIGHTS"] = [struct.unpack('<f', blend_data[n*i+4*j : n*i+4*(j+1)])[0] for j in range(4)]
            self.vb[i]["BLENDINDICES"] = [struct.unpack('<I', blend_data[n*i+16+4*j : n*i+16+4*(j+1)])[0] for j in range(4)]
            
            n = int(self.strides["Texcoord"])
            self.vb[i]["COLOR"] = [struct.unpack('<B', texcoord_data[n*i+j : n*i+j+1])[0]/255 for j in range(4)]
            self.vb[i]["TEXCOORD"] = [struct.unpack('<f', texcoord_data[n*i+4+4*j : n*i+4+4*(j+1)])[0] for j in range(2)]
            if n == 20:
                self.vb[i]["TEXCOORD1"] = [struct.unpack('<f', texcoord_data[n*i+12+4*j : n*i+12+4*(j+1)])[0] for j in range(2)]

    def parse_ibs(self):
        print("Parsing .ib files...")
        self.ibs = {}
        for component in self.first_indices.keys():
            with open(f'{self.mod_name}{component}.ib', 'rb') as f:
                ib_data = f.read()
                vertices = []
                format = '1I' if "32" in self.formats[component + 'IB'] else '1H'
                bytes = 4 if "32" in self.formats[component + 'IB'] else 2
                for i in range(0, len(ib_data), 3*bytes):
                    vertices.append([struct.unpack(format, ib_data[i + bytes * j:i + bytes * (j + 1)])[0] for j in range(3)])
                self.ibs[component] = vertices

    def add_elements(self, vb_text):
        semantic_names = ['POSITION','NORMAL','TANGENT','BLENDWEIGHTS','BLENDINDICES','COLOR','TEXCOORD','TEXCOORD']
        semantic_indices = [0,0,0,0,0,0,0,1]
        formats = ['R32G32B32_FLOAT','R32G32B32_FLOAT','R32G32B32A32_FLOAT','R32G32B32A32_FLOAT','R32G32B32A32_SINT','R8G8B8A8_UNORM','R32G32_FLOAT','R32G32_FLOAT']
        self.offsets = [0,12,24,40,56,72,76,84]
        for i in range(len(self.vb[0].keys())):
            vb_text += f'element[{i}]:\n'
            vb_text += f'  SemanticName: {semantic_names[i]}\n'
            vb_text += f'  SemanticIndex: {semantic_indices[i]}\n'
            vb_text += f'  Format: {formats[i]}\n'
            vb_text += f'  InputSlot: 0\n'
            vb_text += f'  AlignedByteOffset: {self.offsets[i]}\n'
            vb_text += f'  InputSlotClass: per-vertex\n'
            vb_text += f'  InstanceDataStepRate: 0\n'
        return vb_text

    def write_vbs(self):
        print("Writing vb.txt files...")
        stride = sum([int(n) for n in self.strides.values()])
        vb_text = f'stride: {stride}\nfirst vertex: 0\nvertex count: {self.vertex_count}\ntopology: trianglelist\n'
        vb_text = self.add_elements(vb_text)
        vb_text += '\nvertex-data:\n\n'
        for i in range(len(self.vb)):
            for j, (element, values) in enumerate(self.vb[i].items()):
                vb_text += f'vb0[{i}]+{self.offsets[j]:03d} {element}: {", ".join(map(str, map(lambda x: round(x, 9), values)))}\n'
            vb_text += '\n'

        for component in self.first_indices.keys():
            with open(f'{self.mod_name}{component}-vb0={self.hashes["Position"]}.txt', 'w') as f:
                f.write(vb_text)    
            
    def write_ibs(self):
        print("Writing ib.txt files...")
        for component, vertices in self.ibs.items():
            ib_text = f'byte offset: 0\n'
            ib_text += f'first index: {self.first_indices[component]}\n'
            ib_text += f'index count: {len(vertices)*3}\n'
            ib_text += f'topology: trianglelist\n'
            ib_text += f'format: DXGI_FORMAT_R16_UINT\n\n'
            for triplet in vertices:
                ib_text += f'{" ".join(map(str, triplet))}\n'
            with open(f'{self.mod_name}{component}-ib={self.hashes["IB"]}.txt', 'w') as f:
                f.write(ib_text)

    
def main():
    mod = Mod()
    mod.parse_ini()
    mod.parse_buffers()
    mod.parse_ibs()
    mod.write_vbs()
    mod.write_ibs()

if __name__ == '__main__':
    main()