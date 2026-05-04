import { useEffect, useState } from "react";
import { useInsumos } from "../context/InsumosContext";
import {
  getInsumos, createInsumo, updateInsumo,
  deleteInsumo, reactivarInsumo, Insumo,
} from "../services/insumos";
import InsumoModal from "../components/InsumoModal";
import FiltrosInsumos from "../components/FiltrosInsumos";
import TablaInsumos from "../components/TablaInsumos";
import Paginacion from "../components/Paginacion";

export default function InsumosPage() {
  const { state, dispatch } = useInsumos();
  const { insumos, total, skip, limit, filtros, loading } = state;

  const [showModal, setShowModal] = useState(false);
  const [editando, setEditando] = useState<Insumo | null>(null);

  // Estado derivado
  const totalPaginas = Math.ceil(total / limit);
  const paginaActual = Math.floor(skip / limit) + 1;

  // Cargar insumos cuando cambian filtros o paginación
  useEffect(() => {
    const cargar = async () => {
      dispatch({ type: "SET_LOADING", payload: true });
      try {
        const params: Record<string, unknown> = { skip, limit };
        if (filtros.nombre) params.nombre = filtros.nombre;
        if (filtros.activo !== "") params.activo = filtros.activo === "true";
        if (filtros.stockMin) params.stock_min = Number(filtros.stockMin);
        const data = await getInsumos(params);
        dispatch({ type: "SET_INSUMOS", payload: { insumos: data.items, total: data.total } });
      } finally {
        dispatch({ type: "SET_LOADING", payload: false });
      }
    };
    cargar();
  }, [skip, filtros]);

  const abrirCrear = () => { setEditando(null); setShowModal(true); };
  const abrirEditar = (i: Insumo) => { setEditando(i); setShowModal(true); };

  const guardar = async (data: { nombre: string; precio: number; stock: number; activo: boolean }) => {
    if (editando) {
      await updateInsumo(editando.id, data);
    } else {
      await createInsumo(data);
    }
    setShowModal(false);
    dispatch({ type: "SET_SKIP", payload: 0 });
    // Recargar
    const params: Record<string, unknown> = { skip: 0, limit };
    if (filtros.nombre) params.nombre = filtros.nombre;
    if (filtros.activo !== "") params.activo = filtros.activo === "true";
    if (filtros.stockMin) params.stock_min = Number(filtros.stockMin);
    const result = await getInsumos(params);
    dispatch({ type: "SET_INSUMOS", payload: { insumos: result.items, total: result.total } });
  };

  const eliminar = async (id: number) => {
    if (!confirm("¿Eliminar este insumo?")) return;
    await deleteInsumo(id);
    const result = await getInsumos({ skip, limit });
    dispatch({ type: "SET_INSUMOS", payload: { insumos: result.items, total: result.total } });
  };

  const reactivar = async (id: number) => {
    await reactivarInsumo(id);
    const result = await getInsumos({ skip, limit });
    dispatch({ type: "SET_INSUMOS", payload: { insumos: result.items, total: result.total } });
  };

  return (
    <div className="max-w-5xl mx-auto px-4 py-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-6">
        <div>
          <h2 className="text-2xl font-bold text-gray-800">Insumos</h2>
          <p className="text-gray-500 text-sm">{total} insumos encontrados</p>
        </div>
        <button
          onClick={abrirCrear}
          className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg font-semibold transition"
        >
          + Nuevo insumo
        </button>
      </div>

      {/* Filtros */}
      <FiltrosInsumos />

      {/* Tabla */}
      {loading ? (
        <div className="text-center py-12 text-gray-400">Cargando...</div>
      ) : (
        <TablaInsumos
          insumos={insumos}
          onEditar={abrirEditar}
          onEliminar={eliminar}
          onReactivar={reactivar}
        />
      )}

      {/* Paginación */}
      <Paginacion
        paginaActual={paginaActual}
        totalPaginas={totalPaginas}
        total={total}
        onAnterior={() => dispatch({ type: "SET_SKIP", payload: skip - limit })}
        onSiguiente={() => dispatch({ type: "SET_SKIP", payload: skip + limit })}
        skip={skip}
        limit={limit}
      />

      {/* Modal */}
      {showModal && (
        <InsumoModal
          insumo={editando}
          onGuardar={guardar}
          onCerrar={() => setShowModal(false)}
        />
      )}
    </div>
  );
}
