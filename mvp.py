import React, { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Separator } from "@/components/ui/separator";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const compounds = [
  { name: "p-Aminophenol", type: "Primary", mw: 109.13, color: "#9b5de5" },
  { name: "TOLUENE-2,5-DIAMINE SULFATE", type: "Primary", mw: 220.25, color: "#f15bb5" },
  { name: "1-HYDROXYETHYL 4,5-DIAMINO PYRAZOLE SULFATE", type: "Primary", mw: 240.23, color: "#fee440" },
  { name: "N,N-BIS(2-HYDROXYETHYL)-P-PHENYLENEDIAMINE SULFATE", type: "Primary", mw: 312.32, color: "#00bbf9" },
  { name: "m-Aminophenol", type: "Coupler", mw: 109.13, color: "#00f5d4" },
  { name: "Resorcinol", type: "Coupler", mw: 110.11, color: "#9b5de5" },
  { name: "2,4-Diaminophenoxyethanol HCl", type: "Coupler", mw: 241.1, color: "#f15bb5" },
  { name: "2-METHYLRESORCINOL", type: "Coupler", mw: 124.15, color: "#fee440" },
  { name: "4-CHLORORESORCINOL", type: "Coupler", mw: 144.56, color: "#00bbf9" },
  { name: "2-METHYL-5-HYDROXYETHYLAMINOPHENOL", type: "Coupler", mw: 167.21, color: "#00f5d4" },
  { name: "4-AMINO-2-HYDROXYTOLUENE", type: "Coupler", mw: 123.16, color: "#9b5de5" },
  { name: "2-AMINO-4-HYDROXYETHYLAMINOANISOLE SULFATE", type: "Coupler", mw: 279.27, color: "#f15bb5" },
  { name: "1-NAPHTHOL", type: "Coupler", mw: 144.17, color: "#fee440" },
  { name: "2,6-DIHYDROXYETHYLAMINOTOLUENE", type: "Coupler", mw: 210.28, color: "#00bbf9" },
  { name: "HYDROXYETHYL-3,4-METHYLENEDIOXYANILINE HCl", type: "Coupler", mw: 217.65, color: "#00f5d4" },
  { name: "2-AMINO-3-HYDROXYPYRIDINE", type: "Coupler", mw: 110.12, color: "#9b5de5" },
  { name: "4-AMINO-M-CRESOL", type: "Coupler", mw: 123.15, color: "#f15bb5" },
];

const HairDyeCalculator = () => {
  const [precursors, setPrecursors] = useState([]);
  const [couplers, setCouplers] = useState([]);
  const [selectedPrecursor, setSelectedPrecursor] = useState("");
  const [precursorGrams, setPrecursorGrams] = useState("");
  const [selectedCoupler, setSelectedCoupler] = useState("");
  const [couplerGrams, setCouplerGrams] = useState("");

  const addCompound = (type, name, grams) => {
    const compound = compounds.find((c) => c.name === name);
    if (!compound || !grams || isNaN(parseFloat(grams))) return;
    const entry = { ...compound, grams: parseFloat(grams) };
    if (type === "Primary") {
      setPrecursors((prev) => [...prev, entry]);
    } else {
      setCouplers((prev) => [...prev, entry]);
    }
  };

  const updateGrams = (type, index, grams) => {
    const parsed = parseFloat(grams);
    if (isNaN(parsed)) return;
    const updater = (items) => items.map((item, i) => i === index ? { ...item, grams: parsed } : item);
    if (type === "Primary") {
      setPrecursors(updater);
    } else {
      setCouplers(updater);
    }
  };

  const removeEntry = (type, index) => {
    if (type === "Primary") {
      setPrecursors((prev) => prev.filter((_, i) => i !== index));
    } else {
      setCouplers((prev) => prev.filter((_, i) => i !== index));
    }
  };

  const totalMoles = (arr) => arr.reduce((acc, cur) => acc + cur.grams / cur.mw, 0);

  const precursorMoles = totalMoles(precursors);
  const couplerMoles = totalMoles(couplers);
  const ratio = precursorMoles > 0 ? couplerMoles / precursorMoles : 0;

  const predictedShade = () => {
    const tolerance = 0.0000001;
    if (Math.abs(couplerMoles - precursorMoles) <= tolerance) {
      return "✅ Mole match: Ideal for reaction.";
    } else if (precursorMoles > couplerMoles) {
      return "❗ Excess precursor may self-react and deepen the color.";
    } else if (ratio < 1.2) {
      return "Predicted Shade: Light Brown";
    } else if (ratio < 1.5) {
      return "Predicted Shade: Medium Brown";
    } else {
      return "Predicted Shade: Dark Brown";
    }
  };

  const predictedColor = () => {
    if (Math.abs(couplerMoles - precursorMoles) <= 0.0000001) return "#b28f6a";
    if (precursorMoles > couplerMoles) return "#7e5e3c"; // darker
    if (ratio < 1.2) return "#c8ad7f";
    if (ratio < 1.5) return "#8b5e3c";
    return "#4b3621";
  };

  const chartData = [
    { name: "Precursor", moles: Number(precursorMoles.toFixed(4)) },
    { name: "Coupler", moles: Number(couplerMoles.toFixed(4)) },
  ];

  const renderTable = (items, type) => (
    <table className="w-full text-sm mt-4">
      <thead>
        <tr className="text-left border-b">
          <th>Name</th>
          <th>MW</th>
          <th>Grams</th>
          <th>Moles</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        {items.map((item, index) => (
          <tr key={index} className="border-b">
            <td>{item.name}</td>
            <td>{item.mw}</td>
            <td>
              <Input
                type="number"
                value={item.grams}
                onChange={(e) => updateGrams(type, index, e.target.value)}
              />
            </td>
            <td>{(item.grams / item.mw).toFixed(4)}</td>
            <td>
              <Button variant="outline" size="sm" onClick={() => removeEntry(type, index)}>
                Delete
              </Button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );

  return (
    <div className="p-4 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Hair Dye Mole Ratio Calculator</h1>

      <div className="flex flex-col lg:flex-row gap-4">
        <Card className="flex-1">
          <CardContent className="space-y-4">
            <Label>Select Precursor</Label>
            <Select onValueChange={(v) => setSelectedPrecursor(v)}>
              <SelectTrigger>
                <SelectValue placeholder="Select Precursor" />
              </SelectTrigger>
              <SelectContent>
                {compounds.filter((c) => c.type === "Primary").map((compound) => (
                  <SelectItem key={compound.name} value={compound.name}>
                    {compound.name} (MW: {compound.mw})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Input
              type="number"
              placeholder="Enter grams"
              value={precursorGrams}
              onChange={(e) => setPrecursorGrams(e.target.value)}
            />
            <Button onClick={() => {
              addCompound("Primary", selectedPrecursor, precursorGrams);
              setPrecursorGrams("");
            }}>
              Add Precursor
            </Button>
            {renderTable(precursors, "Primary")}
          </CardContent>
        </Card>

        <Card className="flex-1">
          <CardContent className="space-y-4">
            <Label>Select Coupler</Label>
            <Select onValueChange={(v) => setSelectedCoupler(v)}>
              <SelectTrigger>
                <SelectValue placeholder="Select Coupler" />
              </SelectTrigger>
              <SelectContent>
                {compounds.filter((c) => c.type === "Coupler").map((compound) => (
                  <SelectItem key={compound.name} value={compound.name}>
                    {compound.name} (MW: {compound.mw})
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Input
              type="number"
              placeholder="Enter grams"
              value={couplerGrams}
              onChange={(e) => setCouplerGrams(e.target.value)}
            />
            <Button onClick={() => {
              addCompound("Coupler", selectedCoupler, couplerGrams);
              setCouplerGrams("");
            }}>
              Add Coupler
            </Button>
            {renderTable(couplers, "Coupler")}
          </CardContent>
        </Card>
      </div>

      <Separator className="my-4" />

      <Button className="mb-4" onClick={() => {
        setPrecursors([...precursors]);
        setCouplers([...couplers]);
      }}>
        Recalculate
      </Button>

      <div className="text-lg font-semibold">
        Mole Ratio (Coupler / Precursor): {ratio.toFixed(2)}
      </div>
      <div className="text-md mt-2">{predictedShade()}</div>

      <div className="mt-4 w-24 h-10 rounded shadow-md" style={{ backgroundColor: predictedColor() }} />

      <div className="mt-6 h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <XAxis dataKey="name" />
            <YAxis label={{ value: 'Moles', angle: -90, position: 'insideLeft' }} />
            <Tooltip />
            <Bar dataKey="moles" fill="#8884d8" />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default HairDyeCalculator;
