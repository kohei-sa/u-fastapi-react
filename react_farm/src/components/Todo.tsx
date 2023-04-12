import { FC } from 'react';
import { ArrowRightOnRectangleIcon } from '@heroicons/react/24/solid';
import { useProcessAuth } from '../hooks/useProcessAuth';

export const Todo: FC = () => {
  const { logout } = useProcessAuth()
  return (
    <div className="flex justify-center items-center flex-col min-h-screen text-gray-600 font-mono">
      <ArrowRightOnRectangleIcon
        onClick={logout}
        className="h-7 w-7 mt-1 mb-5 text-vlue-500 cursor-pointer"
      />
    </div>
  )
}
