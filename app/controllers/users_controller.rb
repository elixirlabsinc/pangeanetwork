class UsersController < ApplicationController
  def index
    puts 'users index'
    @members = User.not_admin
  end

  def show
    @member = User.find(params[:id])
  end
end
