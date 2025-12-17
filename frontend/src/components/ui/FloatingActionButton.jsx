import { Plus } from 'lucide-react'

export default function FloatingActionButton({ onClick, label = 'Nuevo', icon: Icon = Plus, className = '' }) {
    return (
        <button
            onClick={onClick}
            className={`
                fixed bottom-8 right-8 
                group flex items-center justify-center 
                bg-primary-600 hover:bg-primary-700 text-white 
                shadow-lg hover:shadow-xl 
                rounded-full transition-all duration-300
                z-40
                ${label ? 'px-4 py-3 space-x-2' : 'p-4'}
                ${className}
            `}
            aria-label={label}
        >
            <Icon className="w-6 h-6" />
            {label && (
                <span className="font-semibold text-sm hidden group-hover:inline-block animate-fade-in whitespace-nowrap">
                    {label}
                </span>
            )}
        </button>
    )
}
