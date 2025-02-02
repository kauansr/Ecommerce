import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginPage from './pages/loginpage/LoginPage'
import ProdutosPage from './pages/productpage/ProdutosPage';
import CadastrouserPage from './pages/cadastropage/cadastrouserpage'
import PedidosPage from './pages/pedidospage/PedidosPage';
import UmProduto from './pages/productpage/ProdutoPage';
import UmPedido from './pages/pedidospage/PedidoPage';
import Perfil from './pages/perfilpage/PerfilPage';
import Carrinho from './pages/productpage/Carrinho'
import MinhasAvaliacoes from './pages/productpage/MinhasAvaliacoesPage';
import EditarAvaliacao from './pages/productpage/EditarAvaliacoesPage';

function App() {
  return (
    <div>
      <Router>
        <Routes>
          <Route exact path="/" element={<LoginPage />} />
          <Route exact path="/produtos" element={<ProdutosPage />} />
          <Route exact path="/sign-up" element={<CadastrouserPage />} />
          <Route exact path="/pedidos" element={<PedidosPage />} />
          <Route exact path='/produto/:id' element={<UmProduto />} />
          <Route exact path='/pedido/:id' element={<UmPedido />} />
          <Route exact path='/perfil/:id' element={<Perfil />} />
          <Route exact path='/carrinho' element={<Carrinho />} />
          <Route exact path='/minhas-avaliacoes' element={<MinhasAvaliacoes />} />
          <Route exact path='/avaliacoes/:id' element={<EditarAvaliacao />} />
        </Routes>

      </Router>
    </div >
  );
}

export default App;
