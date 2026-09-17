import { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [alertas, setAlertas] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    const obtenerAlertas = async () => {
      try {
        // Pedir token de la memoria.
        const token = localStorage.getItem('token');

        // Seguridad para que no entren por "casualidad"
        if(!token) {
          navigate('/login');
          return;
        }

        // Peticion GET a backend envaindo el token en Heades
        const respuesta = await axios.get('http://localhost:8000/api/v1/alerts', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        setAlertas(respuesta.data);
        setCargando(false);
      } catch (err) {
        console.error("Error al obtener alertas:", err);
        setError('Acceso denegado o sesion expirada.');
        setCargando(false);

        if(err.response && err.response.status == 401) {
          localStorage.removeItem('token');
          navigate('/login');
        }
      }
    };

    obtenerAlertas();
  }, [navigate]);

  // Funcion para el boton de salir
  const cerrarSesion = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('role');
    navigate('/login');
  };

  
  // Conector de Endpoint PATCH
  const marcarComoAtendida = async (id) => {
    try {
      const token = localStorage.getItem('token');
      
      // Peticion de actualizacion de FastAPI
      await axios.patch(`http://localhost:8000/api/v1/alerts/${id}`, 
        { status: 'Atendida' },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setAlertas(alertas.map(alerta => 
        alerta.id === id ? { ...alerta, status: 'Atendida' } : alerta
      ));

    } catch (err) {
      console.error("Error al actualizar la alerta:", err);
      alert("Hubo un error al intentar actualizar el estatus.");
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '50px auto', fontFamily: 'sans-serif' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h2>Panel de Recursos Humanos</h2>
        <button 
          onClick={cerrarSesion}
          style={{ padding: '8px 12px', backgroundColor: '#ef4444', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}
        >
          Cerrar Sesión
        </button>
      </div>
      <p style={{ color: '#64748b' }}>Monitoreo de incidencias y riesgo de burnout.</p>

      {/* Condicionales de carga y error */}
      {cargando ? (
        <p>Cargando información...</p>
      ) : error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : (
        <div style={{ overflowX: 'auto', marginTop: '20px' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
            <thead>
              <tr style={{ backgroundColor: '#f8fafc', borderBottom: '2px solid #cbd5e1' }}>
                <th style={{ padding: '12px' }}>ID</th>
                <th style={{ padding: '12px' }}>Nivel de Riesgo</th>
                <th style={{ padding: '12px' }}>Motivo detectado por IA</th>
                <th style={{ padding: '12px' }}>Estatus</th>
              </tr>
            </thead>
            <tbody>
              {alertas.length === 0 ? (
                <tr>
                  <td colSpan="4" style={{ padding: '15px', textAlign: 'center', color: '#64748b' }}>
                    Sin alertas registradas por el momento.
                  </td>
                </tr>
              ) : (
                alertas.map((alerta) => (
                  <tr key={alerta.id} style={{ borderBottom: '1px solid #e2e8f0' }}>
                    <td style={{ padding: '12px', color: '#64748b' }}>#{alerta.id}</td>
                    <td style={{ padding: '12px', fontWeight: 'bold', color: alerta.risk_level === 'ALTO' ? '#ef4444' : '#f59e0b' }}>
                      {alerta.risk_level}
                    </td>
                    <td style={{ padding: '12px' }}>{alerta.reason}</td>
                    <td style={{ padding: '12px' }}>
                      <span style={{
                        padding: '4px 8px', borderRadius: '12px', fontSize: '0.85em', fontWeight: 'bold',
                        backgroundColor: alerta.status === 'Atendida' ? '#d1fae5' : '#fee2e2',
                        color: alerta.status === 'Atendida' ? '#059669' : '#b91c1c'
                      }}>
                        {alerta.status}
                      </span>
                    </td>
                    <td style={{ padding: '12px', textAlign: 'center' }}>
                      {/* El botón solo se muestra si el estatus no es "Atendida" */}
                      {alerta.status !== 'Atendida' && (
                        <button
                          onClick={() => marcarComoAtendida(alerta.id)}
                          style={{
                            padding: '6px 12px', backgroundColor: '#3b82f6', color: 'white',
                            border: 'none', borderRadius: '5px', cursor: 'pointer', fontSize: '0.85em'
                          }}
                        >
                          Marcar Atendida
                        </button>
                      )}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default Dashboard;