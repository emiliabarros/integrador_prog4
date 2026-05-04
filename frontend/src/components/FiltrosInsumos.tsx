import { useInsumos } from "../context/InsumosContext";

export default function FiltrosInsumos() {
  const { state, dispatch } = useInsumos();
  const { filtros, insumos } = state;

  // .filter() client-side — estado derivado
  const resumenActivos = insumos.filter((i) => i.activo).length;
  const resumenInactivos = insumos.filter((i) => !i.activo).length;
  const stockBajo = insumos.filter((i) => i.stock < 10).length;

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100 p-4 mb-4">
      <div className="flex justify-between items-center mb-3">
        <h3 className="text-sm font-semibold text-gray-600">Filtros</h3>
        {/* Estado derivado visible */}
        <div className="flex gap-3 text-xs text-gray-500">
          <span className="bg-green-100 text-green-700 px-2 py-0.5 rounded-full">
            {resumenActivos} activos
          </span>
          <span className="bg-red-100 text-red-700 px-2 py-0.5 rounded-full">
            {resumenInactivos} inactivos
          </span>
          {stockBajo > 0 && (
            <span className="bg-yellow-100 text-yellow-700 px-2 py-0.5 rounded-full">
              ⚠️ {stockBajo} con stock bajo
            </span>
          )}
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">

        {/* Filtro nombre */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Nombre</label>
          <input
            type="text"
            placeholder="Buscar por nombre..."
            value={filtros.nombre}
            onChange={(e) => dispatch({ type: "SET_FILTRO_NOMBRE", payload: e.target.value })}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-300"
          />
        </div>

        {/* Filtro activo - Select */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Estado</label>
          <select
            value={filtros.activo}
            onChange={(e) =>
              dispatch({
                type: "SET_FILTRO_ACTIVO",
                payload: e.target.value as "" | "true" | "false",
              })
            }
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-300 bg-white"
          >
            <option value="">Todos</option>
            <option value="true">Activos</option>
            <option value="false">Inactivos</option>
          </select>
        </div>

        {/* Filtro stock mínimo */}
        <div>
          <label className="block text-xs font-medium text-gray-500 mb-1">Stock mínimo</label>
          <input
            type="number"
            placeholder="Ej: 10"
            value={filtros.stockMin}
            onChange={(e) => dispatch({ type: "SET_FILTRO_STOCK_MIN", payload: e.target.value })}
            min="0"
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-red-300"
          />
        </div>
      </div>

      {/* Botón limpiar filtros */}
      {(filtros.nombre || filtros.activo || filtros.stockMin) && (
        <button
          onClick={() => dispatch({ type: "RESET_FILTROS" })}
          className="mt-3 text-xs text-red-500 hover:underline"
        >
          ✕ Limpiar filtros
        </button>
      )}
    </div>
  );
}
