class CoOpsController < ApplicationController
  def index
    @co_ops = CoOp.all
  end

  def show
    @co_op = CoOp.find(params[:id])
  end
end
