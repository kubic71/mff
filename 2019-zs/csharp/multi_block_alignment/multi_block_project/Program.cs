using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace MultiBlockAlignment
{

    public interface IReader
    {

        // return -1 if end of input
        int ReadChar();
        bool EndOfStream { get; }
    }

    public class MultifileReader : IReader
    {
        private int _fileIndex = -1;
        private StreamReader _currentFile = null;
        private string[] inputFiles;

        private bool _endOfFiles = false;

        public MultifileReader(string[] inputFiles)
        {
            // append non-existent file at the end
            this.inputFiles = inputFiles;
        }


        // try to open next file
        // return true it succeded, false if reached end of input file list
        private bool OpenNextFile()
        {
            _fileIndex += 1;
            if (_fileIndex >= inputFiles.Length)
            {
                return false;
            }

            try
            {
                _currentFile = new StreamReader(inputFiles[_fileIndex], Encoding.UTF8);
            } catch (IOException)
            {
                return OpenNextFile();
            }
            
            // empty files are skipped
            if (_currentFile.EndOfStream)
            {
                return OpenNextFile();
            }

            return true;
        }

        
        // returns -1 if reached end of input
        public int ReadChar()
        {
            if (_endOfFiles)
            {
                return -1;
            }

            // put space between two files
            bool outputFileSeparator = false;
            
            if (_currentFile == null)
            {
                _endOfFiles = !OpenNextFile();
            } else if (_currentFile.EndOfStream)
            {
                _endOfFiles = !OpenNextFile();
                outputFileSeparator = true;
            }

            if (outputFileSeparator)
            {
                return ' ';
            } else if (!_endOfFiles)
            {
                char c =  (char)_currentFile.Read();
                if (c == '\r')
                {
                    return ' ';
                }
                return c;
            }
            else
            {
                // edgecase, when no input file is valid, or every is empty
                return ' ';
            }
        }

        public bool EndOfStream => _endOfFiles;
    }
    

    public class Aligner
    {
        private readonly IReader _reader;
        private readonly StreamWriter _outputFile;
        private readonly int _maxLen;
        private readonly bool _highlightSpaces;

        private new List<string> _line;
        private int _lineLength;
        private string NEWLINE = "\n";

        private int _c;
        private StringBuilder _currentWord;
        private bool _blankLine;

        
        public Aligner( IReader reader, string outputFile, int maxLen, bool highlightSpaces)
        {
            this._reader = reader;
            this._outputFile = new StreamWriter(outputFile);
            this._maxLen = maxLen;
            this._highlightSpaces = highlightSpaces;
        }

        private void WriteLine()
        {
            _outputFile.Write(_highlightSpaces ? "<-" + NEWLINE : NEWLINE);
        }

        private void WriteLine(string s)
        {
            Write(s);
            WriteLine();
        }

        private void Write(string s)
        {
            foreach(var c in s)
            {
                if (c == ' ')
                {
                    WriteSpace();
                }
                else
                {
                    _outputFile.Write(c);
                }
            }
        }

        private void WriteSpace()
        {
            _outputFile.Write(_highlightSpaces ? '.' : ' ');
        }

        private void print_line(bool lastParagraphLine)
        {
            if (_line.Count == 0)
            {
                return;
            }
            else if (_line.Count == 1)
            {
                // write one word on its own line, even if it doesn't fit
                WriteLine(_line[0]);
            }
            else
            {
                if (lastParagraphLine)   // word in the last line of a paragraph should be separated only by 1 space
                {
                    for (int j = 0; j < _line.Count; j++)
                    {
                        if (j == _line.Count - 1)
                        {
                            WriteLine(_line[j]);
                        }
                        else
                        {
                            Write(_line[j] + " ");    
                        }
                    }
                }
                else
                {
                    int wordsLen = 0;
                    foreach (var word in _line)
                    {
                        wordsLen += word.Length;
                    }

                    int spareSpaces = _maxLen - wordsLen;
                    int spaceBetweenWords = spareSpaces / (_line.Count - 1) + 1 ;
                    for (int i = 0; i < _line.Count - 1; i++)
                    {
                        Write(_line[i]);
                        
                        int wordSpacesRemaining = _line.Count - 1 - i;
                        if ((spaceBetweenWords-1) * wordSpacesRemaining == spareSpaces)
                        {
                            spaceBetweenWords -= 1;
                        }

                        for (int j = 0; j < spaceBetweenWords; j++)
                        {
                            WriteSpace();
                        }

                        spareSpaces -= spaceBetweenWords;

                    } 
                    
                    Write(_line[_line.Count - 1]);
                    WriteLine();
                }
            }

        }

        public void Process()
        {
            _line = new List<string>();
            _currentWord = new StringBuilder();
            _blankLine = true;

            bool separateParagraphs = false;  // tels me, whether there should be paragraph separation before the next line is printed

            _c = ' ';
            while (_c != -1)
            {
                if (_c == ' ' || _c == '\t' || _c == '\n')
                {
                    if (_currentWord.Length > 0)   // end of word
                    {
                        if (_lineLength + _currentWord.Length > _maxLen)   
                        {
                            // if current word wont fit into the current line, we should print current line and 
                            // then add current word to empty line
                            
                            if (separateParagraphs)
                            {
                                WriteLine();
                                separateParagraphs = false;
                            }
                            
                            print_line(false);  // last_paragraph_line is false, because there will be at lease one more line with current_word in it
                            _line.Clear();
                            _lineLength = 0;
                        }
                        // end of word
                        _line.Add(_currentWord.ToString());
                        _lineLength += _currentWord.Length + 1;
                        _currentWord.Clear();

                    } else if (_c == '\n' && _blankLine) // newline after blank line -> paragraph separation
                    {
                        if (separateParagraphs)
                        {
                            WriteLine();
                        }
                        
                        print_line(true); // print the last line of paragraph
                        _line.Clear();
                        _lineLength = 0;
                        separateParagraphs = true;  
                        
                        // read until some non blank character, in case there are multiple blank lines
                        while (_c == ' ' || _c == '\t' || _c == '\n')
                        {
                            if (_reader.EndOfStream)
                            {
                                _outputFile.Close();
                                return;
                            }
                            _c = _reader.ReadChar();
                        }
                        
                        // c is non-blank
                        _currentWord.Append((char)_c);
                        _blankLine = false;
                    }

                    if (_c == '\n')
                    {
                        _blankLine = true;
                    }
                }
                else
                {
                    // c is non-blank character
                    _blankLine = false;
                    _currentWord.Append((char)_c);
                }

                _c = _reader.ReadChar();
            }

            // current_word is definitely empty, because we added space at the end of the input
            // it may happen, that we still have line to print 
            if (_line.Count > 0)
            {
                if (separateParagraphs)
                {
                    WriteLine();
                }
                print_line(true);
            }
            _outputFile.Close();
        }
    }


    static class Program
    {
        static bool args_are_valid(string[] args)
        {
            if (args.Length < 3)
            {
                return false;
            }

            if (args[0] == "--highlight-spaces")
            {
                if (args.Length < 4)
                    return false;
            }
            
            // check line_length
            if (!int.TryParse(args[args.Length - 1], out int _))
                return false;

            return true;
        }
        
            
        static void Main(string[] args)
            {
                if (!args_are_valid(args))
                {
                    Console.WriteLine("Argument Error");
                    return;
                }

                try
                {
                    bool highlightSpaces = args[0] == "--highlight-spaces";
                    
                    List<string> inputFiles = new List<string>();
                    int i = highlightSpaces ? 1 : 0; 
                    for(; i < args.Length - 2; i++)
                    {
                        inputFiles.Add(args[i]);
                    }

                    string outputFile = args[args.Length - 2];
                    int lineLength = int.Parse(args[args.Length - 1]);
                    
                    Aligner aligner = new Aligner(new MultifileReader(inputFiles.ToArray()), outputFile, lineLength, highlightSpaces);
                    aligner.Process();

                } catch (IOException) {
                    Console.WriteLine("File Error");
                }
            }
    }
}
