import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { Save, Globe, AlertCircle, Check } from 'lucide-react'
import axios from 'axios'

export default function Settings() {
    const queryClient = useQueryClient()
    const [selectedLanguage, setSelectedLanguage] = useState('es')
    const [successMsg, setSuccessMsg] = useState('')

    // Fetch supported languages
    const { data: languages, isLoading } = useQuery({
        queryKey: ['languages'],
        queryFn: async () => {
            const res = await axios.get('/api/v1/i18n/languages/')
            return res.data
        }
    })

    // Fetch current dictionary (simulation of "active" language)
    // Ideally this state should be global (Context)
    useEffect(() => {
        const storedLang = localStorage.getItem('app_language')
        if (storedLang) setSelectedLanguage(storedLang)
    }, [])

    const handleLanguageChange = async (code) => {
        setSelectedLanguage(code)
        localStorage.setItem('app_language', code)

        // Fetch new dictionary to cache it
        try {
            await axios.get(`/api/v1/i18n/dictionary/${code}`)
            setSuccessMsg('Idioma actualizado correctamente')
            setTimeout(() => setSuccessMsg(''), 3000)

            // In a real app, we would update the Context here
            // For MVP, we can reload to apply heavy changes or just show success
        } catch (err) {
            console.error(err)
        }
    }

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex items-center justify-between">
                <h1 className="text-3xl font-bold text-gray-900">Configuración</h1>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Language Settings */}
                <div className="card">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="p-2 bg-blue-100 rounded-lg">
                            <Globe className="w-6 h-6 text-blue-600" />
                        </div>
                        <div>
                            <h2 className="text-xl font-bold text-gray-900">Idioma y Región</h2>
                            <p className="text-sm text-gray-500">Configura el lenguaje del sistema</p>
                        </div>
                    </div>

                    {successMsg && (
                        <div className="mb-4 p-3 bg-green-50 text-green-700 rounded-lg flex items-center gap-2">
                            <Check className="w-4 h-4" />
                            {successMsg}
                        </div>
                    )}

                    <div className="space-y-4">
                        <label className="label">Idioma del Sistema</label>
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                            {isLoading ? (
                                <p className="text-sm text-gray-400">Cargando idiomas...</p>
                            ) : (
                                languages?.map(lang => (
                                    <button
                                        key={lang.code}
                                        onClick={() => handleLanguageChange(lang.code)}
                                        className={`flex items-center justify-between p-4 rounded-xl border transition-all ${selectedLanguage === lang.code
                                                ? 'border-primary bg-primary-50 text-primary ring-2 ring-primary ring-offset-2'
                                                : 'border-gray-200 hover:border-gray-300 hover:bg-gray-50'
                                            }`}
                                    >
                                        <div className="flex items-center gap-3">
                                            <span className="text-2xl">{lang.code === 'es' ? '🇪🇸' : lang.code === 'en' ? '🇺🇸' : '🏳️'}</span>
                                            <span className="font-medium">{lang.name}</span>
                                        </div>
                                        {selectedLanguage === lang.code && (
                                            <Check className="w-5 h-5" />
                                        )}
                                    </button>
                                ))
                            )}
                        </div>
                        <p className="text-xs text-gray-500 mt-2">
                            * Esto cambiará los textos de la interfaz y formateará fechas/monedas.
                        </p>
                    </div>
                </div>

                {/* Placeholder for other settings */}
                <div className="card opacity-50 pointer-events-none grayscale">
                    <div className="flex items-center gap-3 mb-6">
                        <div className="p-2 bg-gray-100 rounded-lg">
                            <Save className="w-6 h-6 text-gray-600" />
                        </div>
                        <div>
                            <h2 className="text-xl font-bold text-gray-900">General</h2>
                            <p className="text-sm text-gray-500">Próximamente...</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}
