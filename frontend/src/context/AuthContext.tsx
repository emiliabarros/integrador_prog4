import { createContext, useContext, useReducer, useEffect, ReactNode } from "react";

// --- Tipos ---
interface Usuario {
  id: number;
  nombre: string;
  email: string;
}

interface AuthState {
  usuario: Usuario | null;
  token: string | null;
  isAuthenticated: boolean;
}

type AuthAction =
  | { type: "LOGIN"; payload: { usuario: Usuario; token: string } }
  | { type: "LOGOUT" };

// --- Estado inicial desde localStorage ---
const initialState: AuthState = {
  token: localStorage.getItem("token"),
  usuario: null,
  isAuthenticated: !!localStorage.getItem("token"),
};

// --- Reducer ---
function authReducer(state: AuthState, action: AuthAction): AuthState {
  switch (action.type) {
    case "LOGIN":
      localStorage.setItem("token", action.payload.token);
      return {
        token: action.payload.token,
        usuario: action.payload.usuario,
        isAuthenticated: true,
      };
    case "LOGOUT":
      localStorage.removeItem("token");
      return {
        token: null,
        usuario: null,
        isAuthenticated: false,
      };
    default:
      return state;
  }
}

// --- Context ---
interface AuthContextType {
  state: AuthState;
  dispatch: React.Dispatch<AuthAction>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// --- Provider ---
export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Cargar usuario desde el token al iniciar
  useEffect(() => {
    if (state.token && !state.usuario) {
      import("../services/auth").then(({ getMe }) => {
        getMe()
          .then((usuario) => {
            dispatch({ type: "LOGIN", payload: { usuario, token: state.token! } });
          })
          .catch(() => {
            dispatch({ type: "LOGOUT" });
          });
      });
    }
  }, []);

  return (
    <AuthContext.Provider value={{ state, dispatch }}>
      {children}
    </AuthContext.Provider>
  );
}

// --- Hook personalizado ---
export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth debe usarse dentro de AuthProvider");
  return context;
}
