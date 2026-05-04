import { Insumo } from "../services/insumos";

interface Props {
  insumos: Insumo[];
  onEditar: (i: Insumo) => void;
  onEliminar: (id: number) => void;
  onReactivar: (id: number) => void;
}

export default function TablaInsumos({ insumos, onEditar, onEliminar, onReactivar }: Props) {
  if (insumos.length === 0) {
    return (
      <div className="text-center py-12 text-gray-400 bg-white rounded-xl border border-gray-100">
        No se encontraron insumos
      </div>
    );
  }

  return (
    <div className="overflow-x-auto rounded-xl shadow-sm border border-gray-100">
      <table className="w-full bg-white text-sm">
        <thead className="bg-gray-50 text-gray-600 uppercase text-xs">
          <tr>
            <th className="px-4 py-3 text-left">ID</th>
            <th className="px-4 py-3 text-left">Nombre</th>
            <th className="px-4 py-3 text-left">Precio</th>
            <th className="px-4 py-3 text-left">Stock</th>
            <th className="px-4 py-3 text-left">Estado</th>
            <th className="px-4 py-3 text-left">Acciones</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-100">
          {insumos.map((insumo) => (
            <tr key={insumo.id} className="hover:bg-gray-50 transition">
              <td className="px-4 py-3 text-gray-400">#{insumo.id}</td>
              <td className="px-4 py-3 font-medium text-gray-800">{insumo.nombre}</td>
              <td className="px-4 py-3 text-gray-700">${insumo.precio.toFixed(2)}</td>
              <td className="px-4 py-3">
                <span className={`font-semibold ${insumo.stock < 10 ? "text-red-500" : "text-gray-700"}`}>
                  {insumo.stock}
                </span>
              </td>
              <td className="px-4 py-3">
                <span
                  className={`px-2 py-1 rounded-full text-xs font-semibold ${
                    insumo.activo
                      ? "bg-green-100 text-green-700"
                      : "bg-red-100 text-red-700"
                  }`}
                >
                  {insumo.activo ? "Activo" : "Inactivo"}
                </span>
              </td>
              <td className="px-4 py-3">
                <div className="flex gap-2">
                  <button
                    onClick={() => onEditar(insumo)}
                    className="bg-blue-500 hover:bg-blue-600 text-white text-xs px-3 py-1 rounded-lg transition"
                  >
                    Editar
                  </button>
                  {insumo.eliminado_en ? (
                    <button
                      onClick={() => onReactivar(insumo.id)}
                      className="bg-green-500 hover:bg-green-600 text-white text-xs px-3 py-1 rounded-lg transition"
                    >
                      Reactivar
                    </button>
                  ) : (
                    <button
                      onClick={() => onEliminar(insumo.id)}
                      className="bg-red-500 hover:bg-red-600 text-white text-xs px-3 py-1 rounded-lg transition"
                    >
                      Eliminar
                    </button>
                  )}
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
