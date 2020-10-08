using System;
using System.Collections.Generic;
using System.Diagnostics;
using Microsoft.VisualBasic.CompilerServices;
using Microsoft.VisualBasic.FileIO;

namespace P7.Models
{
    public class WineStore : DataSystem<Wine>
    {
        private string file;

        // Constructor.
        public WineStore(string filePath)
        {
            this.file = filePath;
        }

        // Returns list of Wines.
        public List<Wine> Read(Func<string[], bool> pred)
        {
            List<Wine> wines = new List<Wine>();

            using (TextFieldParser parser = new TextFieldParser(this.file))
            {
                parser.TextFieldType = FieldType.Delimited;
                parser.SetDelimiters(",");

                while (!parser.EndOfData)
                {
                    string[] fields = parser.ReadFields();

                    if (pred(fields))
                        wines.Add(BuildWine(fields));
                }
            }

            return wines;
        }

        // Builds Wine instance from .cvs fields.
        private static Wine BuildWine(string[] csvFiels)
        {
            return new Wine(csvFiels[0], Double.Parse(csvFiels[2]), csvFiels[3],
                Int16.Parse(csvFiels[5]), Int16.Parse(csvFiels[6]), csvFiels[4],
                csvFiels[7], Int16.Parse(csvFiels[1]), Int32.Parse(csvFiels[8]));
        }
    }
}