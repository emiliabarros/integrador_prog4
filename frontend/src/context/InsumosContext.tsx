import { createContext, useContext, useReducer, ReactNode } from "react";
import { Insumo } from "../services/insumos";

// --- Tipos ---
interface FiltrosState {
  nombre: string;
  activo: "" | "true" | "false";
  stockMin: string;
}

interface InsumosState {
  insumos: Insumo[];
  total: number;
  skip: number;
  limit: number;
  filtros: FiltrosState;
  loading: boolean;
}

type InsumosAction =
  | { type: "SET_INSUMOS"; payload: { insumos: Insumo[]; total: number } }
  | { type: "SET_LOADING"; payload: boolean }
  | { type: "SET_FILTRO_NOMBRE"; payload: string }
  | { type: "SET_FILTRO_ACTIVO"; payload: "" | "true" | "false" }
  | { type: "SET_FILTRO_STOCK_MIN"; payload: string }
  | { type: "SET_SKIP"; payload: number }
  | { type: "RESET_FILTROS" };

// --- Estado inicial ---
const initialState: InsumosState = {
  insumos: [],
  total: 0,
  skip: 0,
  limit: 5,
  filtros: { nombre: "", activo: "", stockMin: "" },
  loading: false,
};

// --- Reducer ---
function insumosReducer(state: InsumosState, action: InsumosAction): InsumosState {
  switch (action.type) {
    case "SET_INSUMOS":
      return { ...state, insumos: action.payload.insumos, total: action.payload.total };
    case "SET_LOADING":
      return { ...state, loading: action.payload };
    case "SET_FILTRO_NOMBRE":
      return { ...state, filtros: { ...state.filtros, nombre: action.payload }, skip: 0 };
    case "SET_FILTRO_ACTIVO":
      return { ...state, filtros: { ...state.filtros, activo: action.payload }, skip: 0 };
    case "SET_FILTRO_STOCK_MIN":
      return { ...state, filtros: { ...state.filtros, stockMin: action.payload }, skip: 0 };
    case "SET_SKIP":
      return { ...state, skip: action.payload };
    case "RESET_FILTROS":
      return { ...state, filtros: { nombre: "", activo: "", stockMin: "" }, skip: 0 };
    default:
      return state;
  }
}

// --- Context ---
interface InsumosContextType {
  state: InsumosState;
  dispatch: React.Dispatch<InsumosAction>;
}

const InsumosContext = createContext<InsumosContextType | undefined>(undefined);

// --- Provider ---
export function InsumosProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(insumosReducer, initialState);
  return (
    <InsumosContext.Provider value={{ state, dispatch }}>
      {children}
    </InsumosContext.Provider>
  );
}

// --- Hook personalizado ---
export function useInsumos() {
  const context = useContext(InsumosContext);
  if (!context) throw new Error("useInsumos debe usarse dentro de InsumosProvider");
  return context;
}
