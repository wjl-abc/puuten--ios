//
//  LibViewController.h
//  puuten
//
//  Created by wang jialei on 12-8-17.
//
//

#import <UIKit/UIKit.h>
#import "WaterFlowView.h"
#import "ImageViewCell.h"
#import "Constance.h"

@interface LibViewController : UIViewController<WaterFlowViewDelegate, WaterFlowViewDataSource>
{
    NSMutableArray *arrayData;
    NSMutableArray *array4wb;
    WaterFlowView  *waterFlow;
    int selected_cell;
    int selected_order;
}

- (void)dataSourceDidLoad;
- (void)dataSourceDidError;

@end
