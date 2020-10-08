using System;
using System.Collections.Generic;

namespace P7.Models
{
    public interface DataSystem<OT>
    {
        List<OT> Read(Func<string[], bool> pred);
    }
}