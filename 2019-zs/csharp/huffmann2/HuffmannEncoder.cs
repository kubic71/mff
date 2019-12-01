using System;
using System.Collections.Generic;
using System.IO;
using System.Runtime.CompilerServices;
using System.Security.Cryptography;

namespace huffmann
{
    
    class BitWriter
    {
        private int bufferPos = 0;
        static int BUFFER_SIZE = 4096;  // MUST be divisible by 8
        private byte[] buffer = new byte[BUFFER_SIZE];
        private Stream outputStream;

        public BitWriter(Stream outputStream)
        {
            this.outputStream = outputStream;
        }
        
        
        // array of bytes, where each value if either 0 or 1 
        public void WriteBits(byte[] bits) 
        {
            foreach (var bit in bits)
            {
                buffer[bufferPos] = bit;
                bufferPos++;
                if (bufferPos == BUFFER_SIZE)
                {
                    Flush();
                    bufferPos = 0;
                } 
            }
        }

        // flush the buffer
        public void Flush()
        {
            int bytesToWrite = bufferPos % 8 == 0 ? bufferPos / 8 : bufferPos / 8 + 1; 
            for (int i = 0; i < bytesToWrite; i++)
            {
                byte toWrite = (byte)(buffer[i * 8] | buffer[i * 8 + 1] << 1 | buffer[i * 8 + 2] << 2 | buffer[i * 8 + 3] << 3 |
                    buffer[i * 8 + 4] << 4 | buffer[i * 8 + 5] << 5 | buffer[i * 8 + 6] << 6 | buffer[i * 8 + 7] << 7);
                
                outputStream.WriteByte(toWrite);
            }
        }
    }
    public class HuffmannEncoder
    {
        public static void Encode(Stream inputStream, Stream outputStream)
        {
            HuffmannTree huffmannTree = HuffmannTree.BuildTree(inputStream);
            outputStream.Write(new byte[]{0x7B, 0x68, 0x75, 0x7C, 0x6D, 0x7D, 0x66, 0x66}); // write header
            
            huffmannTree.PrintTree(outputStream, true);
            outputStream.Write(new byte[]{0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00}); // huffmann tree representation is ended with 8 bytes of zeros
            
            inputStream.Position = 0;

            EncodeData(inputStream, outputStream, huffmannTree);
        }

        public static void EncodeData(Stream inputStream, Stream outputStream, HuffmannTree huffmannTree)
        {
            int b; 
            BitWriter writer = new BitWriter(outputStream);
            while((b=inputStream.ReadByte()) != -1)
            {
                byte[] path = huffmannTree.paths[(char) b];

                /*
                foreach (var bit in path)
                {
                    Console.Write(bit);
                }
                Console.WriteLine();
                */
                
                
                writer.WriteBits(path);
            }
            
            writer.Flush();
        }
    }
}