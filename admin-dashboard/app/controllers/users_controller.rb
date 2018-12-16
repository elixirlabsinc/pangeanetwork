class UsersController < ApplicationController
  def index
    puts 'users index'
    @members = User.not_admin
  end

  def show
    @member = User.find(params[:id])
  end

  def new
    @user = User.new
  end

  def create
    @user = User.new(create_params)
    @user.save
    redirect_to users_path
  end

  def create_params
    params.require(:user).permit(:first_name, :last_name, :email, :phone, :co_op_id, :role_id)
  end
end
