"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [cats, setCats] = useState([]);
  const [form, setForm] = useState({ name: "", experience_years: "", breed: "", salary: "" });
  const [breeds, setBreeds] = useState([]);
  const API = "http://127.0.0.1:8000";

  
  const fetchCats = async () => {
    const res = await fetch(`${API}/cats`);
    setCats(await res.json());
  };


  const fetchBreeds = async () => {
    const res = await fetch("https://api.thecatapi.com/v1/breeds");
    const data = await res.json();
    setBreeds(data.map(b => b.name));
  };

  useEffect(() => {
    fetchCats();
    fetchBreeds();
  }, []);


  const addCat = async (e) => {
    e.preventDefault();
    if (!form.name.trim() || /^\d+$/.test(form.name)) {
      alert("Name must contain letters, not just numbers");
      return;
    }
    if (!form.experience_years || form.experience_years <= 0) { alert("Experience must be > 0"); return; }
    if (!form.breed) { alert("Breed is required"); return; }
    if (!form.salary || form.salary <= 0) { alert("Salary must be > 0"); return; }
    try {
      const res = await fetch(`${API}/cats`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });
      if (!res.ok) throw new Error(await res.text());
      setForm({ name: "", experience_years: 0, breed: "", salary: 0 });
      fetchCats();
    } catch (err) { alert("Error: " + err.message); }
  };


  const updateSalary = async (id) => {
    const newSalary = prompt("New salary?");
    if (!newSalary) return;
    await fetch(`${API}/cats/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ salary: parseFloat(newSalary) }),
    });
    fetchCats();
  };


  const deleteCat = async (id) => {
    if (!confirm("Delete this cat?")) return;
    await fetch(`${API}/cats/${id}`, { method: "DELETE" });
    fetchCats();
  };

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto", padding: "1rem" }}>
      <h1 style={{ fontSize: "1.5rem", marginBottom: "1rem" }}>Spy Cats Dashboard</h1>

      <form onSubmit={addCat} style={{ marginBottom: "1.5rem" }}>
        <input 
          type="text" 
          placeholder="Name" 
          value={form.name} 
          onChange={e => setForm({...form,name:e.target.value})} 
          style={{ display: "block", width: "100%", marginBottom: "0.5rem", padding: "0.5rem" }}
        />

        <input 
          type="number" 
          placeholder="Experience Years" 
          value={form.experience_years} 
          onChange={e => setForm({...form,experience_years:e.target.value})} 
          style={{ display: "block", width: "100%", marginBottom: "0.5rem", padding: "0.5rem" }}
        />

        <select 
          value={form.breed} 
          onChange={e => setForm({...form, breed: e.target.value})} 
          style={{ display: "block", width: "100%", marginBottom: "0.5rem", padding: "0.5rem" }}
        >
          <option value="">Select breed</option>
          {breeds.map(b => <option key={b} value={b}>{b}</option>)}
        </select>

        <input 
          type="number" 
          placeholder="Salary" 
          value={form.salary} 
          onChange={e => setForm({...form,salary:e.target.value})} 
          style={{ display: "block", width: "100%", marginBottom: "0.5rem", padding: "0.5rem" }}
        />

        <button type="submit" style={{ backgroundColor: "#3b82f6", color: "#fff", padding: "0.5rem 1rem", border: "none", cursor: "pointer" }}>Add Cat</button>
      </form>

      <table style={{ width: "100%", borderCollapse: "collapse" }}>
        <thead>
          <tr style={{ backgroundColor: "#e5e7eb" }}>
            <th style={{ border: "1px solid #ccc", padding: "0.5rem" }}>Name</th>
            <th style={{ border: "1px solid #ccc", padding: "0.5rem" }}>Exp</th>
            <th style={{ border: "1px solid #ccc", padding: "0.5rem" }}>Breed</th>
            <th style={{ border: "1px solid #ccc", padding: "0.5rem" }}>Salary</th>
            <th style={{ border: "1px solid #ccc", padding: "0.5rem" }}>Actions</th>
          </tr>
        </thead>
        <tbody>
          {cats.map(cat => (
            <tr key={cat.id}>
              <td style={{ border: "1px solid #ccc", padding: "0.5rem" }}>{cat.name}</td>
              <td style={{ border: "1px solid #ccc", padding: "0.5rem" }}>{cat.experience_years}</td>
              <td style={{ border: "1px solid #ccc", padding: "0.5rem" }}>{cat.breed}</td>
              <td style={{ border: "1px solid #ccc", padding: "0.5rem" }}>{cat.salary}</td>
              <td style={{ border: "1px solid #ccc", padding: "0.5rem" }}>
                <button onClick={()=>updateSalary(cat.id)} style={{ marginRight: "0.5rem", color: "#2563eb", cursor: "pointer" }}>Edit</button>
                <button onClick={()=>deleteCat(cat.id)} style={{ color: "#dc2626", cursor: "pointer" }}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
