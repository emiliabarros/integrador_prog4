import { useState, useEffect } from "react";
import { Insumo } from "../services/insumos";

interface Props {
  insumo: Insumo | null;
  onGuardar: (data: { nombre: string; precio: number; stock: number; activo: boolean }) => Promise<void>;
  onCerrar: () => void;
}

export default function InsumoModal({ insumo, onGuardar, onCerrar }: Props) {
  const [form, setForm] = useState({
    nombre: "",
    precio: "",
    stock: "",
    activo: true,
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  // Cargar datos si estamos editando
  useEffect(() => {
    if (insumo) {
      setForm({
        nombre: insumo.nombre,
        precio: String(insumo.precio),
        stock: String(insumo.stock),
        activo: insumo.activo,
      });
    }
  }, [insumo]);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value, type, checked } = e.target;
    setForm({ ...form, [name]: type === "checkbox" ? checked : value });
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await onGuardar({
        nombre: form.nombre,
        precio: Number(form.precio),
        stock: Number(form.stock),
        activo: form.activo,
      });
    } catch {
      setError("Error al guardar. Revisá los datos.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 px-4">
      <div className="bg-white rounded-2xl shadow-xl w-full max-w-md p-6">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-bold text-gray-800">
            {insumo ? "Editar insumo" : "Nuevo insumo"}
          </h3>
          <button onClick={onCerrar} className="text-gray-400 hover:text-gray-600 text-xl">✕</button>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-4">
          {/* Nombre */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-1">Nombre</label>
            <input
              type="text"
              name="nombre"
              value={form.nombre}
              onChange={handleChange}
              placeholder="Ej: Pan brioche"
              required
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-300"
            />
          </div>

          {/* Precio y Stock en grid */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Precio ($)</label>
              <input
                type="number"
                name="precio"
                value={form.precio}
                onChange={handleChange}
                placeholder="0.00"
                required
                min="0"
                step="0.01"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-300"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Stock</label>
              <input
                type="number"
                name="stock"
                value={form.stock}
                onChange={handleChange}
                placeholder="0"
                required
                min="0"
                className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-300"
              />
            </div>
          </div>

          {/* Activo - Checkbox */}
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              name="activo"
              id="activo"
              checked={form.activo}
              onChange={handleChange}
              className="w-4 h-4 accent-red-500"
            />
            <label htmlFor="activo" className="text-sm font-medium text-gray-700 cursor-pointer">
              Insumo activo
            </label>
          </div>

          {error && (
            <p className="text-red-500 text-sm bg-red-50 border border-red-200 rounded-lg px-3 py-2">
              {error}
            </p>
          )}

          <div className="flex gap-3 pt-2">
            <button
              type="submit"
              disabled={loading}
              className="flex-1 bg-red-600 hover:bg-red-700 text-white font-semibold py-2 rounded-lg transition disabled:opacity-60"
            >
              {loading ? "Guardando..." : "Guardar"}
            </button>
            <button
              type="button"
              onClick={onCerrar}
              className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 font-semibold py-2 rounded-lg transition"
            >
              Cancelar
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
