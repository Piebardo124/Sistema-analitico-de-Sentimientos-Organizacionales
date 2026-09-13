import {useState} from 'react';
import axios from 'axios';

function App() {
  const [texto, setTexto] = useState('');
  const [analisis, setAnalisis] = useState(null);
  const [cargando, setCargando] = useState(null);

  const manejarEnvio = async (e) => {
    e.preventDefault(); // Evita que la pagina recargue
    setCargando(true);
    setAnalisis(null);

    try {
      // Logica de React para llamar a FastAPI en Docker
      const respuetsa = await axios.post('http://localhost:8000/api/v1/nlp/analyze-feedback', {
        text_content: texto
      });

      // Logica de guardado de respuesta para mostrar en pantalla
      setAnalisis(respuetsa.data.ai_analysis);
    } catch (error) {
      console.error("Error al enviar:", error);
      alert("Hubo un error de conexion, revisar Consola (F12)")
    }

    setCargando(false);
  };

  return(
    <div style={{ maxWidth: '600px', margin: '50px auto', fontFamily: 'sans-serif', textAlign: 'center' }}>
      <h1>PluriOne - Buzón Inteligente</h1>
      <p>Escribe tu comentario corporativo y la IA lo analizará.</p>

      <form onSubmit={manejarEnvio} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
        <textarea
          rows="5"
          placeholder="Ej. El ambiente es muy pesado y el jefe me grita. Mi número es 6621998877..."
          value={texto}
          onChange={(e) => setTexto(e.target.value)}
          style={{ padding: '10px', fontSize: '16px', borderRadius: '5px' }}
          required
        />
        <button
          type="submit"
          disabled={cargando}
          style={{ 
            padding: '12px', fontSize: '16px', backgroundColor: '#2563eb', 
            color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' 
          }}
        >
          {cargando ? 'Analizando con IA...' : 'Enviar Comentario'}
        </button>
      </form>

      {/* Esta sección solo aparece si la IA ya nos respondió */}
      {analisis && (
        <div style={{ marginTop: '30px', padding: '20px', border: '1px solid #ccc', borderRadius: '8px', backgroundColor: '#f8fafc', textAlign: 'left' }}>
          <h3 style={{ marginTop: '0', color: '#0f172a' }}>Resultado del Análisis:</h3>
          <p><strong>Sentimiento:</strong> {analisis.label}</p>
          <p><strong>Score de Polaridad:</strong> {analisis.polarity}</p>
          <p><strong>Emoción principal:</strong> {analisis.details.emocion}</p>
          <p><strong>Riesgo de Burnout:</strong> {analisis.details.riesgo_burnout ? "ALTO" : "Bajo"}</p>
        </div>
      )}
    </div>
  );
}

export default App;