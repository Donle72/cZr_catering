import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Ingredients from './pages/Ingredients'
import Recipes from './pages/Recipes'
import RecipeDetail from './pages/RecipeDetail'
import Events from './pages/Events'
import Suppliers from './pages/Suppliers'

function App() {
    return (
        <Router>
            <Layout>
                <Routes>
                    <Route path="/" element={<Dashboard />} />
                    <Route path="/ingredients" element={<Ingredients />} />
                    <Route path="/recipes" element={<Recipes />} />
                    <Route path="/recipes/:id" element={<RecipeDetail />} />
                    <Route path="/events" element={<Events />} />
                    <Route path="/suppliers" element={<Suppliers />} />
                </Routes>
            </Layout>
        </Router>
    )
}

export default App
