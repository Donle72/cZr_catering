import { useState, useEffect, useRef } from 'react'
import { Search, Loader2, Check } from 'lucide-react'
import axios from 'axios'
import { useDebounce } from '../../hooks/useDebounce'

export default function SmartCombobox({
    value,
    onChange,
    placeholder = "Buscar ingrediente...",
    endpoint = "/api/v1/search/ingredients"
}) {
    const [searchTerm, setSearchTerm] = useState('')
    const [results, setResults] = useState([])
    const [isLoading, setIsLoading] = useState(false)
    const [isOpen, setIsOpen] = useState(false)
    const [selectedItem, setSelectedItem] = useState(null)

    const debouncedSearch = useDebounce(searchTerm, 300)
    const wrapperRef = useRef(null)

    // Handle outside click to close
    useEffect(() => {
        function handleClickOutside(event) {
            if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
                setIsOpen(false)
            }
        }
        document.addEventListener("mousedown", handleClickOutside)
        return () => document.removeEventListener("mousedown", handleClickOutside)
    }, [wrapperRef])

    // Search Effect
    useEffect(() => {
        if (debouncedSearch.length < 2) {
            setResults([])
            return
        }

        const fetchResults = async () => {
            setIsLoading(true)
            try {
                const res = await axios.get(endpoint, {
                    params: { q: debouncedSearch, limit: 10 }
                })
                setResults(res.data)
                setIsOpen(true)
            } catch (error) {
                console.error("Search failed", error)
            } finally {
                setIsLoading(false)
            }
        }

        fetchResults()
    }, [debouncedSearch, endpoint])

    const handleSelect = (item) => {
        setSelectedItem(item)
        setSearchTerm(item.name) // Display name
        onChange(item.id) // Return ID to parent form
        setIsOpen(false)
    }

    return (
        <div className="relative w-full" ref={wrapperRef}>
            <div className="relative">
                <input
                    type="text"
                    className="input pl-10 w-full"
                    placeholder={placeholder}
                    value={searchTerm}
                    onChange={(e) => {
                        setSearchTerm(e.target.value)
                        setIsOpen(true)
                    }}
                    onFocus={() => {
                        if (results.length > 0) setIsOpen(true)
                    }}
                />
                <div className="absolute left-3 top-1/2 transform -translate-y-1/2">
                    {isLoading ? (
                        <Loader2 className="w-5 h-5 text-gray-400 animate-spin" />
                    ) : (
                        <Search className="w-5 h-5 text-gray-400" />
                    )}
                </div>
            </div>

            {/* Dropdown Results */}
            {isOpen && results.length > 0 && (
                <div className="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-xl max-h-60 overflow-y-auto">
                    <ul className="py-1">
                        {results.map((item) => (
                            <li
                                key={item.id}
                                onClick={() => handleSelect(item)}
                                className="px-4 py-2 hover:bg-blue-50 cursor-pointer flex justify-between items-center group transition-colors"
                            >
                                <div>
                                    <div className="font-medium text-gray-900">{item.name}</div>
                                    <div className="text-xs text-gray-500">
                                        {item.sku && <span className="mr-2">SKU: {item.sku}</span>}
                                        <span className="bg-gray-100 px-1 rounded">{item.unit_symbol}</span>
                                        <span className="ml-2 text-green-600">${item.current_cost?.toFixed(2)}</span>
                                    </div>
                                </div>
                                {value === item.id && <Check className="w-4 h-4 text-primary" />}
                            </li>
                        ))}
                    </ul>
                </div>
            )}

            {/* No items state */}
            {isOpen && !isLoading && searchTerm.length >= 2 && results.length === 0 && (
                <div className="absolute z-50 w-full mt-1 bg-white border border-gray-200 rounded-lg shadow-xl p-4 text-center text-sm text-gray-500">
                    No se encontraron ingredientes.
                </div>
            )}
        </div>
    )
}
