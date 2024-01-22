import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/loginpage/LoginPage'
import ProdutosPage from './pages/productpage/ProdutosPage';
import CadastrouserPage from './pages/cadastropage/cadastrouserpage'
import PedidosPage from './pages/pedidospage/PedidosPage';
import UmProduto from './pages/productpage/ProdutoPage';

function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route exact path="/login" element={<LoginPage />} />
          <Route exact path="/produtos" element={<ProdutosPage />} />
          <Route exact path="/sign-up" element={<CadastrouserPage />} />
          <Route exact path="/pedidos" element={<PedidosPage />} />
          <Route exact path='/produto/:id' element={<UmProduto />} />
        </Routes>

      </Router>
    </div>
  );
}

export default App;
