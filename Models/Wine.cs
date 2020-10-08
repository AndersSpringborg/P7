namespace P7.Models
{
    public class Wine
    {
        public string Name { get;  }
        public double Price { get; } // Must be the same currency.
        public string Region { get; }
        public short Year { get; }
        public short CriticsScore { get; }
        public string Producer { get; }
        public string Type { get; }
        public short Volume { get; } // Expressed in milliliters.
        public int Lwin { get; }

        // Constructor.
        public Wine(string name, double price, string region, short year, short score, string producer, string type, short volume, int lwin)
        {
            this.Name = name;
            this.Price = price;
            this.Region = region;
            this.Year = year;
            this.CriticsScore = score;
            this.Producer = producer;
            this.Type = type;
            this.Volume = volume;
            this.Lwin = lwin;
        }

        // Overriden ToString() method.
        public override string ToString()
        {
            return "Name: " + this.Name + " - Price: " + this.Price + " - Region: " + this.Region + " - Year: " + this.Year + " - Critics score: " + this.CriticsScore + " - Producer: " + this.Producer + " - Type: " + this.Type + " - Volume: " + this.Volume + " - LWIN: " + this.Lwin;
        }

        // Overriden equals method.
        public override bool Equals(object obj)
        {
            if (obj == null || !this.GetType().Equals(obj.GetType()))
                return false;

            return this.Lwin == ((Wine) obj).Lwin;
        }
    }
}