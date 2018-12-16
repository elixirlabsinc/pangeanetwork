class CoOpsController < ApplicationController
  def index
    @co_ops = CoOp.all
  end

  def show
    @co_op = CoOp.find(params[:id])
  end

  def create
    @co_op = CoOp.new(create_params)
    if @co_op.save
      redirect_to co_ops_path
    else
      flash[:error] = @co_op.errors.full_messages
    end
  end

  def new
    @co_op = CoOp.new
  end

  def create_params
    params.require(:co_op).permit(:name, :phase_id, :is_active, :start_date, :end_date, :location, :interest, :initial_balance, :expected_repayment, :current_balance)
  end
end
