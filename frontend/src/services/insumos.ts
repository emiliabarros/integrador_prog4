import api from "./api";

export interface Insumo {
  id: number;
  nombre: string;
  precio: number;
  stock: number;
  activo: boolean;
  eliminado_en: string | null;
}

export interface InsumoCreate {
  nombre: string;
  precio: number;
  stock: number;
}

export interface InsumoListParams {
  nombre?: string;
  activo?: boolean;
  stock_min?: number;
  skip?: number;
  limit?: number;
}

export const getInsumos = async (params: InsumoListParams = {}) => {
  const res = await api.get("/insumos", { params });
  return res.data as { total: number; items: Insumo[] };
};

export const getInsumo = async (id: number) => {
  const res = await api.get(`/insumos/${id}`);
  return res.data as Insumo;
};

export const createInsumo = async (data: InsumoCreate) => {
  const res = await api.post("/insumos", data);
  return res.data as Insumo;
};

export const updateInsumo = async (id: number, data: Partial<InsumoCreate>) => {
  const res = await api.put(`/insumos/${id}`, data);
  return res.data as Insumo;
};

export const deleteInsumo = async (id: number) => {
  await api.delete(`/insumos/${id}`);
};

export const reactivarInsumo = async (id: number) => {
  const res = await api.patch(`/insumos/${id}/reactivar`);
  return res.data as Insumo;
};
