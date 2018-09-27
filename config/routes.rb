Rails.application.routes.draw do
  get 'page/index'
  root to: 'page#index'

  resources :transactions
  resources :users
  resources :co_ops
  resources :loans
end
